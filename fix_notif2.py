with open('gui/main_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

notif_btn = '''
        # Notification bell
        self.notif_btn = tk.Button(
            title_frame,
            text="🔔",
            font=("Helvetica", 13),
            bg="#2d1f00",
            fg="#FFD700",
            relief="flat",
            padx=8,
            pady=5,
            cursor="hand2",
            command=self.show_notifications
        )
        self.notif_btn.pack(side="right", padx=5)
'''

code = code.replace(
    '        # Add Refresh button',
    notif_btn + '        # Add Refresh button'
)

notif_method = '''
    def show_notifications(self):
        import json, os, tkinter as tk
        nf = os.path.join(os.path.dirname(__file__), '..', 'data', 'notifications.json')
        if not os.path.exists(nf):
            tk.messagebox.showinfo("Notifications", "No notifications yet.")
            return
        with open(nf) as f:
            notifs = json.load(f)
        mine = [n for n in notifs if n.get("user") == self.account.name]
        if not mine:
            tk.messagebox.showinfo("Notifications", "No notifications for you yet.")
            return
        unread = [n for n in mine if not n.get("seen")]
        msg = ""
        for n in mine[-5:]:
            status = "" if n.get("seen") else " [NEW]"
            msg += f"{status} {n.get('message', '')}\\n\\n"
        # Mark all as seen
        for n in notifs:
            if n.get("user") == self.account.name:
                n["seen"] = True
        with open(nf, "w") as f:
            json.dump(notifs, f, indent=2)
        self.notif_btn.config(fg="#FFD700")
        tk.messagebox.showinfo(f"Notifications ({len(unread)} new)", msg.strip())

'''

code = code.replace(
    '    def refresh(self):',
    notif_method + '    def refresh(self):'
)

with open('gui/main_window.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Done!')
