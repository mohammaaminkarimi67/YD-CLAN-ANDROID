import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path
import json, hashlib

APP_DIR = Path(__file__).resolve().parent
BACKGROUND = APP_DIR / "yd_military_background.png"
DATA_FILE = APP_DIR / "yd_clan_data.json"
ADMIN_PIN_HASH = hashlib.sha256("YD2026".encode("utf-8")).hexdigest()

DEFAULT_MEMBERS = [
    {"name":"VICTOR","role":"Leader","level":"150","status":"آنلاین"},
    {"name":"PARSA","role":"Co-Leader","level":"150","status":"آنلاین"},
    {"name":"seyed","role":"Co-Leader","level":"147","status":"آنلاین"},
    {"name":"rezabruski","role":"Veteran","level":"143","status":"آفلاین"},
    {"name":"mmd","role":"Veteran","level":"141","status":"آنلاین"},
    {"name":"mobin","role":"Veteran","level":"139","status":"آفلاین"},
    {"name":"abol","role":"Member","level":"138","status":"آنلاین"},
    {"name":"","role":"Member","level":"137","status":"آفلاین"},
    {"name":"Eagle","role":"Member","level":"136","status":"آنلاین"},
    {"name":"Flame","role":"Member","level":"135","status":"آنلاین"},
    {"name":"Storm","role":"Member","level":"134","status":"آفلاین"},
    {"name":"Venom","role":"Member","level":"133","status":"آنلاین"},
    {"name":"Titan","role":"Member","level":"132","status":"آنلاین"},
    {"name":"Nightmare","role":"Member","level":"131","status":"آفلاین"},
    {"name":"Blaze","role":"Member","level":"130","status":"آنلاین"},
    {"name":"Killer","role":"Member","level":"129","status":"آنلاین"},
    {"name":"Maverick","role":"Member","level":"128","status":"آفلاین"},
    {"name":"Viper","role":"Member","level":"127","status":"آنلاین"},
    {"name":"Sniper","role":"Member","level":"126","status":"آنلاین"},
    {"name":"Phantom","role":"Member","level":"125","status":"آنلاین"},
]

def load_data():
    if DATA_FILE.exists():
        try:
            d = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(d.get("members"), list) and isinstance(d.get("requests", []), list):
                return {"members": d["members"][:20], "requests": d.get("requests", [])}
        except (OSError, json.JSONDecodeError):
            pass
    return {"members": DEFAULT_MEMBERS.copy(), "requests": []}

DATA = load_data()

class YDClanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YD CLAN | مدیریت کلن")
        self.root.geometry("1120x720")
        self.root.minsize(850, 560)
        self.admin = False
        self.bg_photo = None
        self.bg_label = None
        self.original_bg = None
        try:
            from PIL import Image, ImageTk
            if BACKGROUND.exists():
                self.Image, self.ImageTk = Image, ImageTk
                self.original_bg = Image.open(BACKGROUND).convert("RGB")
                self.resize_bg()
                self.root.bind("<Configure>", self.on_resize)
        except ImportError:
            messagebox.showwarning("Pillow", "برای نمایش تصویر پس‌زمینه CMD را باز کن و اجرا کن: py -m pip install pillow")
        self.root.configure(bg="#101214")
        self.build_ui()
        self.refresh_members()

    def resize_bg(self):
        if self.original_bg is None: return
        w, h = max(self.root.winfo_width(), 850), max(self.root.winfo_height(), 560)
        resized = self.original_bg.resize((w, h), self.Image.Resampling.LANCZOS)
        self.bg_photo = self.ImageTk.PhotoImage(resized)
        if self.bg_label is None:
            self.bg_label = tk.Label(self.root, image=self.bg_photo, bd=0)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
        else:
            self.bg_label.configure(image=self.bg_photo)

    def on_resize(self, event):
        if event.widget == self.root and self.original_bg is not None: self.resize_bg()

    def button(self, parent, text, command, color):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                         activebackground=color, activeforeground="white", relief="flat",
                         bd=0, padx=12, pady=7, cursor="hand2")

    def build_ui(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Treeview", background="#17191b", foreground="white",
                        fieldbackground="#17191b", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#292c30", foreground="#ff4545",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#8e2020")])
        header = tk.Frame(self.root, bg="#090a0b", highlightbackground="#a52a2a", highlightthickness=1)
        header.pack(fill="x", padx=16, pady=(16, 10))
        tk.Label(header, text="ỾƊ CLAN", fg="#ff3838", bg="#090a0b",
                 font=("Segoe UI", 24, "bold")).pack(side="left", padx=18, pady=12)
        tk.Label(header, text="TOGETHER WE RISE  •  ظرفیت: 20 نفر", fg="white", bg="#090a0b",
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=8)
        self.mode_label = tk.Label(header, text="حالت مشاهده", fg="#cccccc", bg="#090a0b")
        self.mode_label.pack(side="right", padx=15)
        panel = tk.Frame(self.root, bg="#101214", highlightbackground="#555555", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        bar = tk.Frame(panel, bg="#101214"); bar.pack(fill="x", padx=12, pady=10)
        tk.Label(bar, text="فهرست اعضای کلن", fg="white", bg="#101214",
                 font=("Segoe UI", 16, "bold")).pack(side="left")
        self.button(bar, "درخواست عضویت", self.join_request, "#a52222").pack(side="right", padx=4)
        self.button(bar, "ورود مدیر", self.admin_login, "#34383d").pack(side="right", padx=4)
        self.logout_btn = self.button(bar, "خروج مدیر", self.admin_logout, "#34383d")
        self.logout_btn.pack(side="right", padx=4); self.logout_btn.pack_forget()
        wrap = tk.Frame(panel, bg="#101214"); wrap.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        cols = ("no","name","role","level","status")
        self.table = ttk.Treeview(wrap, columns=cols, show="headings")
        for col, title, width in [("no","شماره",70),("name","نام داخل بازی",300),("role","سمت",220),("level","لول",100),("status","وضعیت",150)]:
            self.table.heading(col, text=title); self.table.column(col, width=width, anchor="center")
        scroll = ttk.Scrollbar(wrap, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        self.admin_bar = tk.Frame(panel, bg="#101214")
        self.button(self.admin_bar,"افزودن عضو",self.add_member,"#256b39").pack(side="left",padx=3)
        self.button(self.admin_bar,"حذف عضو انتخاب‌شده",self.remove_member,"#8f2424").pack(side="left",padx=3)
        self.button(self.admin_bar,"بررسی درخواست‌ها",self.review_requests,"#34383d").pack(side="left",padx=3)
        self.admin_bar.pack(fill="x", padx=12, pady=(0,10)); self.admin_bar.pack_forget()
        tk.Label(self.root, text="YD CLAN • نسخه محلی؛ اطلاعات فقط روی همین کامپیوتر ذخیره می‌شود",
                 fg="white", bg="#090a0b", font=("Segoe UI",9)).pack(fill="x",padx=16,pady=(0,10))

    def save(self):
        DATA_FILE.write_text(json.dumps(DATA, ensure_ascii=False, indent=2), encoding="utf-8")

    def refresh_members(self):
        for row in self.table.get_children(): self.table.delete(row)
        for i,m in enumerate(DATA["members"],1):
            self.table.insert("","end",values=(i,m.get("name",""),m.get("role","Member"),m.get("level","-"),m.get("status","آفلاین")))

    def admin_login(self):
        pin = simpledialog.askstring("ورود مدیر","رمز مدیر را وارد کن:",show="*")
        if pin is None: return
        if hashlib.sha256(pin.encode("utf-8")).hexdigest() == ADMIN_PIN_HASH:
            self.admin = True; self.mode_label.config(text="حالت مدیر فعال",fg="#64e879")
            self.admin_bar.pack(fill="x",padx=12,pady=(0,10)); self.logout_btn.pack(side="right",padx=4)
            messagebox.showinfo("موفق","حالت مدیر فعال شد.")
        else: messagebox.showerror("خطا","رمز اشتباه است.")

    def admin_logout(self):
        self.admin = False; self.mode_label.config(text="حالت مشاهده",fg="#cccccc")
        self.admin_bar.pack_forget(); self.logout_btn.pack_forget()

    def join_request(self):
        if len(DATA["members"]) >= 20:
            messagebox.showinfo("ظرفیت کامل","کلن ۲۰ عضو دارد."); return
        name = simpledialog.askstring("درخواست عضویت","نام داخل بازی (IGN):")
        if not name or not name.strip(): return
        name = name.strip()
        if any(m.get("name","").casefold()==name.casefold() for m in DATA["members"]):
            messagebox.showwarning("تکراری","این نام عضو کلن است."); return
        if any(r.get("name","").casefold()==name.casefold() for r in DATA["requests"]):
            messagebox.showinfo("تکراری","درخواست این نام قبلاً ثبت شده."); return
        DATA["requests"].append({"name":name}); self.save()
        messagebox.showinfo("ثبت شد","درخواست ذخیره شد؛ مدیر باید بررسی کند.")

    def add_member(self):
        if not self.admin: return
        if len(DATA["members"]) >= 20:
            messagebox.showwarning("ظرفیت کامل","حداکثر ۲۰ عضو."); return
        name = simpledialog.askstring("افزودن عضو","نام داخل بازی:")
        if not name or not name.strip(): return
        name = name.strip()
        if any(m.get("name","").casefold()==name.casefold() for m in DATA["members"]):
            messagebox.showwarning("تکراری","این عضو از قبل وجود دارد."); return
        level = simpledialog.askstring("لول عضو","لول عضو:",initialvalue="1") or "1"
        DATA["members"].append({"name":name,"role":"Member","level":level,"status":"آفلاین"})
        self.save(); self.refresh_members()

    def remove_member(self):
        if not self.admin: return
        selected = self.table.selection()
        if not selected: messagebox.showwarning("انتخاب عضو","اول یک عضو انتخاب کن."); return
        idx = int(self.table.item(selected[0],"values")[0])-1
        if idx == 0: messagebox.showwarning("محدودیت","رهبر کلن را از این نسخه نمی‌توان حذف کرد."); return
        name = DATA["members"][idx]["name"]
        if messagebox.askyesno("تأیید",f"عضو {name} حذف شود؟"):
            DATA["members"].pop(idx); self.save(); self.refresh_members()

    def review_requests(self):
        if not self.admin: return
        if not DATA["requests"]: messagebox.showinfo("درخواست‌ها","درخواستی وجود ندارد."); return
        names = "\n".join("• "+r.get("name","") for r in DATA["requests"])
        if messagebox.askyesno("درخواست‌ها",names+"\n\nاولین درخواست را تأیید می‌کنی؟"):
            if len(DATA["members"])>=20: messagebox.showwarning("ظرفیت کامل","کلن ۲۰ عضو دارد."); return
            req=DATA["requests"].pop(0)
            DATA["members"].append({"name":req["name"],"role":"Member","level":"1","status":"آفلاین"})
            self.save(); self.refresh_members(); messagebox.showinfo("تأیید شد",req["name"]+" اضافه شد.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YDClanApp(root)
    root.mainloop()
