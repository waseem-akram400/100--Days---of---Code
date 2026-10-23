
import tkinter as tk
import random
import time


# ٹائپنگ کے لیے مختلف جملے
SENTENCES = [
    "Python is a great programming language.",
    "Practice makes progress every day.",
    "Learning to code takes time and patience.",
    "Small steps can lead to big achievements.",
    "Keep learning and never stop improving."
]


class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 86 - Typing Speed Test")
        self.root.geometry("750x600")
        self.root.minsize(650, 500)
        self.root.configure(bg="#172033")

        self.start_time = None
        self.timer_running = False
        self.test_finished = False
        self.target_sentence = ""

        title = tk.Label(
            root,
            text="Typing Speed Test",
            font=("Arial", 26, "bold"),
            bg="#172033",
            fg="white"
        )
        title.pack(pady=(20, 8))

        subtitle = tk.Label(
            root,
            text="Type the sentence below as quickly and accurately as you can.",
            font=("Arial", 11),
            bg="#172033",
            fg="#cbd5e1"
        )
        subtitle.pack(pady=(0, 15))

        self.sentence_label = tk.Label(
            root,
            text="",
            font=("Arial", 16),
            wraplength=650,
            justify="left",
            bg="#26334d",
            fg="white",
            padx=20,
            pady=20
        )
        self.sentence_label.pack(fill="x", padx=25, pady=10)

        self.input_box = tk.Text(
            root,
            height=5,
            font=("Consolas", 14),
            wrap="word",
            padx=12,
            pady=12,
            bg="#ffffff",
            fg="#172033",
            insertbackground="#172033",
            relief="flat"
        )
        self.input_box.pack(fill="x", padx=25, pady=10)
        self.input_box.bind("<KeyRelease>", self.check_typing)

        # اعدادوشمار دکھانے کے لیے
        stats_frame = tk.Frame(root, bg="#172033")
        stats_frame.pack(fill="x", padx=25, pady=15)

        self.time_label = self.make_stat(stats_frame, "Time", "0 sec")
        self.wpm_label = self.make_stat(stats_frame, "Speed", "0 WPM")
        self.accuracy_label = self.make_stat(
            stats_frame, "Accuracy", "100%"
        )
        self.errors_label = self.make_stat(stats_frame, "Errors", "0")

        self.status_label = tk.Label(
            root,
            text="Press Start Test to begin.",
            font=("Arial", 12, "bold"),
            bg="#172033",
            fg="#93c5fd"
        )
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(
            root,
            text="Start Test",
            font=("Arial", 12, "bold"),
            bg="#38bdf8",
            fg="#172033",
            activebackground="#7dd3fc",
            relief="flat",
            padx=25,
            pady=10,
            command=self.start_test
        )
        self.start_button.pack(pady=10)

        self.reset_button = tk.Button(
            root,
            text="New Sentence / Reset",
            font=("Arial", 11),
            bg="#334155",
            fg="white",
            activebackground="#475569",
            relief="flat",
            padx=18,
            pady=8,
            command=self.reset_test
        )
        self.reset_button.pack(pady=(0, 15))

        self.reset_test()

    def make_stat(self, parent, heading, initial_value):
        """ایک اعدادوشمار کا لیبل بناتا ہے۔"""
        frame = tk.Frame(parent, bg="#26334d", padx=10, pady=12)
        frame.pack(side="left", expand=True, fill="x", padx=5)

        tk.Label(
            frame,
            text=heading,
            font=("Arial", 10),
            bg="#26334d",
            fg="#cbd5e1"
        ).pack()

        value_label = tk.Label(
            frame,
            text=initial_value,
            font=("Arial", 16, "bold"),
            bg="#26334d",
            fg="white"
        )
        value_label.pack(pady=(5, 0))

        return value_label

    def start_test(self):
        """ٹیسٹ شروع کرتا ہے اور ٹائپنگ باکس فعال کرتا ہے۔"""
        self.reset_test()
        self.start_time = time.time()
        self.timer_running = True
        self.input_box.config(state="normal")
        self.input_box.focus_set()
        self.status_label.config(
            text="Start typing! The timer is running.",
            fg="#86efac"
        )
        self.start_button.config(state="disabled")
        self.update_timer()

    def reset_test(self):
        """نیا جملہ منتخب کرکے ٹیسٹ دوبارہ تیار کرتا ہے۔"""
        self.timer_running = False
        self.test_finished = False
        self.start_time = None
        self.target_sentence = random.choice(SENTENCES)

        self.sentence_label.config(text=self.target_sentence)
        self.input_box.config(state="normal")
        self.input_box.delete("1.0", tk.END)
        self.input_box.config(state="disabled")

        self.time_label.config(text="0 sec")
        self.wpm_label.config(text="0 WPM")
        self.accuracy_label.config(text="100%")
        self.errors_label.config(text="0")

        self.status_label.config(
            text="Press Start Test to begin.",
            fg="#93c5fd"
        )
        self.start_button.config(state="normal")

    def check_typing(self, event=None):
        """ٹائپ کیے گئے حروف کا اصل جملے سے موازنہ کرتا ہے۔"""
        if not self.timer_running or self.test_finished:
            return

        typed_text = self.input_box.get("1.0", "end-1c")
        elapsed = max(time.time() - self.start_time, 0.01)

        # ہر درست حرف گنیں
        correct_chars = 0
        for index, char in enumerate(typed_text):
            if (
                index < len(self.target_sentence)
                and char == self.target_sentence[index]
            ):
                correct_chars += 1

        # غلط حروف کی تعداد
        errors = len(typed_text) - correct_chars

        # WPM: درست حروف کو 5 سے تقسیم کرکے منٹ کے حساب سے
        minutes = elapsed / 60
        wpm = int((correct_chars / 5) / minutes) if minutes > 0 else 0

        # Accuracy فیصد
        if len(typed_text) > 0:
            accuracy = (correct_chars / len(typed_text)) * 100
        else:
            accuracy = 100

        self.wpm_label.config(text=f"{wpm} WPM")
        self.accuracy_label.config(text=f"{accuracy:.1f}%")
        self.errors_label.config(text=str(errors))

        # پورا جملہ ٹائپ ہوجائے تو ٹیسٹ ختم کریں
        if typed_text == self.target_sentence:
            self.finish_test(elapsed, wpm, accuracy)

    def update_timer(self):
        """ہر سیکنڈ کے بعد وقت تازہ کرتا ہے۔"""
        if self.timer_running and self.start_time is not None:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"{elapsed} sec")
            self.root.after(250, self.update_timer)

    def finish_test(self, elapsed, wpm, accuracy):
        """ٹیسٹ مکمل ہونے پر نتیجہ دکھاتا ہے۔"""
        self.timer_running = False
        self.test_finished = True
        self.input_box.config(state="disabled")
        self.start_button.config(state="normal")

        self.time_label.config(text=f"{elapsed:.1f} sec")
        self.status_label.config(
            text=f"Test complete! Speed: {wpm} WPM | Accuracy: {accuracy:.1f}%",
            fg="#86efac"
        )


if __name__ == "__main__":
    window = tk.Tk()
    app = TypingSpeedTest(window)
    window.mainloop()
