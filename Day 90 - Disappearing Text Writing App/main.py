import tkinter as tk
from tkinter import messagebox


class DisappearingTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 90 - Disappearing Text")
        self.root.geometry("800x600")
        self.root.configure(bg="#18212f")
        self.root.minsize(600, 450)

        self.time_limit = 5
        self.remaining = self.time_limit
        self.timer_id = None
        self.started = False
        self.finished = False

        tk.Label(
            root,
            text="The Dangerous Writing App",
            font=("Arial", 24, "bold"),
            bg="#18212f",
            fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            root,
            text="Keep writing. Stop too long and your words disappear!",
            font=("Arial", 11),
            bg="#18212f",
            fg="#b8c4d9"
        ).pack(pady=(0, 15))

        self.timer_label = tk.Label(
            root,
            text=f"Idle time left: {self.time_limit}s",
            font=("Arial", 14, "bold"),
            bg="#18212f",
            fg="#fbbf24"
        )
        self.timer_label.pack(pady=5)

        self.text_box = tk.Text(
            root,
            font=("Consolas", 14),
            wrap="word",
            padx=15,
            pady=15,
            bg="#f8fafc",
            fg="#18212f",
            insertbackground="#18212f",
            undo=True
        )
        self.text_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )
        self.text_box.bind("<KeyPress>", self.on_typing)

        bottom = tk.Frame(root, bg="#18212f")
        bottom.pack(pady=(0, 15))

        tk.Button(
            bottom,
            text="Start / Continue",
            command=self.start_writing,
            font=("Arial", 11, "bold"),
            bg="#38bdf8",
            fg="#18212f",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            bottom,
            text="Restart",
            command=self.restart,
            font=("Arial", 11, "bold"),
            bg="#334155",
            fg="white",
            padx=15,
            pady=8
        ).pack(side="left", padx=5)

        tk.Label(
            root,
            text="The timer resets whenever you type. Pause too long and the text is cleared.",
            font=("Arial", 9),
            bg="#18212f",
            fg="#b8c4d9"
        ).pack(pady=(0, 12))

    def start_writing(self):
        if self.finished:
            self.restart()

        if not self.started:
            self.started = True
            self.text_box.focus_set()
            self.reset_timer()

    def on_typing(self, event=None):
        if self.finished:
            return

        if not self.started:
            self.started = True

        self.reset_timer()

    def reset_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.remaining = self.time_limit
        self.update_timer()

    def update_timer(self):
        if not self.started or self.finished:
            return

        self.timer_label.config(
            text=f"Idle time left: {self.remaining}s"
        )

        if self.remaining <= 0:
            self.clear_text()
            return

        self.remaining -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    def clear_text(self):
        self.finished = True
        self.started = False
        self.timer_id = None

        self.text_box.delete("1.0", tk.END)
        self.timer_label.config(
            text="Your text disappeared!",
            fg="#fb7185"
        )
        messagebox.showwarning(
            "Time is up!",
            "You stopped typing for too long. Your text has been cleared."
        )

    def restart(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        self.text_box.delete("1.0", tk.END)
        self.remaining = self.time_limit
        self.started = False
        self.finished = False

        self.timer_label.config(
            text=f"Idle time left: {self.time_limit}s",
            fg="#fbbf24"
        )
        self.text_box.focus_set()


if __name__ == "__main__":
    window = tk.Tk()
    app = DisappearingTextApp(window)
    window.mainloop()
