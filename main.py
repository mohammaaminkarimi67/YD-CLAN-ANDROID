from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.clearcolor = (0.035, 0.035, 0.04, 1)

MEMBERS = [
    ("Negan", "Leader", "139"),
    ("Reaper", "Veteran", "139"),
    ("Shadow", "Member", "138"),
    ("Samurai", "Member", "137"),
    ("Eagle", "Member", "136"),
    ("Flame", "Member", "135"),
    ("Storm", "Member", "134"),
    ("Venom", "Member", "133"),
    ("Titan", "Member", "132"),
    ("Nightmare", "Member", "131"),
    ("Blaze", "Member", "130"),
    ("Killer", "Member", "129"),
    ("Maverick", "Member", "128"),
    ("Viper", "Member", "127"),
    ("Sniper", "Member", "126"),
    ("Phantom", "Member", "125"),
    ("Raven", "Member", "124"),
    ("Ghost", "Member", "123"),
    ("Hunter", "Member", "122"),
    ("Frost", "Member", "121"),
]

KV = r"""
#:import dp kivy.metrics.dp
ScreenManager:
    HomeScreen:
    RequestScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: 0.035, 0.035, 0.04, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(58)
            spacing: dp(10)
            Label:
                text: "YD CLAN"
                color: 1, 0.12, 0.16, 1
                bold: True
                font_size: "28sp"
                halign: "left"
                text_size: self.size
            Label:
                text: "TOGETHER WE RISE"
                color: 0.92, 0.92, 0.92, 1
                font_size: "11sp"
                halign: "right"
                text_size: self.size
        Label:
            text: "اعضای کلن  •  ظرفیت ۲۰ نفر"
            size_hint_y: None
            height: dp(32)
            color: 1, 0.2, 0.22, 1
            bold: True
            font_size: "18sp"
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: member_list
                cols: 1
                spacing: dp(6)
                padding: dp(2)
                size_hint_y: None
                height: self.minimum_height
        Button:
            text: "درخواست عضویت"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: 0.75, 0.05, 0.09, 1
            color: 1, 1, 1, 1
            bold: True
            on_release: app.root.current = "request"
        Label:
            text: "نسخه آزمایشی — درخواست‌ها هنوز آنلاین نیستند"
            size_hint_y: None
            height: dp(26)
            color: 0.7, 0.7, 0.7, 1
            font_size: "10sp"

<RequestScreen>:
    name: "request"
    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(12)
        canvas.before:
            Color:
                rgba: 0.035, 0.035, 0.04, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "درخواست عضویت YD"
            size_hint_y: None
            height: dp(54)
            color: 1, 0.12, 0.16, 1
            bold: True
            font_size: "23sp"
        Label:
            text: "نام داخل بازی"
            size_hint_y: None
            height: dp(28)
            halign: "right"
            text_size: self.size
        TextInput:
            id: player_name
            hint_text: "مثلاً: YourName"
            multiline: False
            size_hint_y: None
            height: dp(48)
            background_color: 0.12, 0.12, 0.14, 1
            foreground_color: 1, 1, 1, 1
            cursor_color: 1, 0.15, 0.18, 1
        Label:
            text: "لول بازی"
            size_hint_y: None
            height: dp(28)
            halign: "right"
            text_size: self.size
        TextInput:
            id: player_level
            hint_text: "مثلاً: 120"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: dp(48)
            background_color: 0.12, 0.12, 0.14, 1
            foreground_color: 1, 1, 1, 1
        Label:
            id: result
            text: "این نسخه نمایشی است؛ ارسال آنلاین در مرحله بعد اضافه می‌شود."
            color: 0.9, 0.7, 0.25, 1
            halign: "center"
            valign: "middle"
            text_size: self.size
        Button:
            text: "ثبت آزمایشی"
            size_hint_y: None
            height: dp(50)
            background_normal: ""
            background_color: 0.75, 0.05, 0.09, 1
            on_release: app.preview_request()
        Button:
            text: "بازگشت به اعضا"
            size_hint_y: None
            height: dp(44)
            background_normal: ""
            background_color: 0.2, 0.2, 0.22, 1
            on_release: app.root.current = "home"
"""

class HomeScreen(Screen):
    pass

class RequestScreen(Screen):
    pass

class YDClanApp(App):
    def build(self):
        root = Builder.load_string(KV)
        listing = root.get_screen("home").ids.member_list
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.graphics import Color, RoundedRectangle

        for idx, (name, role, level) in enumerate(MEMBERS, start=1):
            row = BoxLayout(size_hint_y=None, height=dp(44), padding=(dp(10), 0), spacing=dp(8))
            with row.canvas.before:
                Color(0.10, 0.10, 0.12, 1)
                rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[dp(6)])
            row.bind(pos=lambda inst, val, r=rect: setattr(r, "pos", val),
                     size=lambda inst, val, r=rect: setattr(r, "size", val))
            row.add_widget(Label(text=str(idx), size_hint_x=0.12, color=(1, .22, .25, 1), font_size="12sp"))
            row.add_widget(Label(text=name, size_hint_x=0.42, color=(1, 1, 1, 1), halign="left", font_size="14sp"))
            row.add_widget(Label(text=role, size_hint_x=0.28, color=(.78, .78, .8, 1), font_size="11sp"))
            row.add_widget(Label(text=level, size_hint_x=0.18, color=(1, 1, 1, 1), font_size="12sp"))
            listing.add_widget(row)
        return root

    def preview_request(self):
        screen = self.root.get_screen("request")
        name = screen.ids.player_name.text.strip()
        level = screen.ids.player_level.text.strip()
        if not name:
            screen.ids.result.text = "لطفاً نام داخل بازی را وارد کن."
        elif not level:
            screen.ids.result.text = "لطفاً لول بازی را وارد کن."
        else:
            screen.ids.result.text = f"درخواست آزمایشی برای {name} آماده است؛ هنوز آنلاین ارسال نمی‌شود."

if __name__ == "__main__":
    from kivy.metrics import dp
    YDClanApp().run()
