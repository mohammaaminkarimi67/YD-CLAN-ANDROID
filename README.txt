YD CLAN ANDROID — Stage 1
=========================

This is a UI prototype for Android, built with Python + Kivy.

Current features:
- Dark red/black YD CLAN screen
- Sample roster of 20 players
- Join request form (local preview only)
- Portrait layout

IMPORTANT:
- Requests are NOT online in this stage.
- Admin login and secure member management are NOT implemented yet.
- Do not publish this prototype as a production app.
- Stage 2 will connect a hosted database/backend and enforce admin-only permissions server-side.

Build APK:
Recommended beginner route: upload this folder to a GitHub repository, then use the Actions tab
to run "Build YD CLAN APK". The workflow file is included in .github/workflows/android.yml.
The APK appears under the completed workflow's Artifacts section.

Requirements for local testing:
  python -m pip install kivy
  python main.py

Next step:
Configure an online backend (e.g. Supabase/Firebase) with:
- members table (max 20 active members)
- join_requests table
- admin authentication and database security rules
Never place admin passwords or service-role keys inside the APK.
