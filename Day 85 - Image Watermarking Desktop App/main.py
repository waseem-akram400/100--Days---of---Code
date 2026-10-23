import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day 85 - Image Watermarking App")
        self.root.geometry("900x700")
        self.root.minsize(650, 550)
        self.root.configure(bg="#eef2f7")

        self.original_image = None
        self.image_path = None
        self.preview_photo = None

        self.watermark_text = tk.StringVar(value="© Waseem Akram")
        self.position = tk.StringVar(value="Bottom Right")
        self.opacity = tk.IntVar(value=160)
        self.font_size = tk.IntVar(value=32)

        self.build_interface()

    def build_interface(self):
        heading = tk.Label(
            self.root,
            text="IMAGE WATERMARKING APP",
            font=("Arial", 20, "bold"),
            bg="#eef2f7",
            fg="#172554"
        )
        heading.pack(pady=(18, 5))

        subtitle = tk.Label(
            self.root,
            text="Open an image, add your watermark, and save a new copy.",
            font=("Arial", 10),
            bg="#eef2f7",
            fg="#475569"
        )
        subtitle.pack(pady=(0, 12))

        controls = tk.Frame(self.root, bg="#eef2f7")
        controls.pack(fill="x", padx=22)

        tk.Button(
            controls,
            text="Choose Image",
            command=self.choose_image,
            bg="#2563eb",
            fg="white",
            padx=12,
            pady=7
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.file_label = tk.Label(
            controls,
            text="No image selected",
            bg="#eef2f7",
            fg="#475569",
            anchor="w"
        )
        self.file_label.grid(row=0, column=1, sticky="ew", padx=8)

        tk.Label(
            controls, text="Watermark text:",
            bg="#eef2f7"
        ).grid(row=1, column=0, padx=5, pady=8, sticky="w")

        tk.Entry(
            controls,
            textvariable=self.watermark_text,
            font=("Arial", 11),
            width=30
        ).grid(row=1, column=1, sticky="ew", padx=8)

        tk.Label(
            controls, text="Position:",
            bg="#eef2f7"
        ).grid(row=2, column=0, padx=5, pady=8, sticky="w")

        positions = [
            "Bottom Right", "Bottom Left", "Top Right",
            "Top Left", "Center"
        ]
        position_menu = ttk.Combobox(
            controls,
            textvariable=self.position,
            values=positions,
            state="readonly",
            width=18
        )
        position_menu.grid(row=2, column=1, sticky="w", padx=8)
        position_menu.bind("<<ComboboxSelected>>", self.update_preview)

        tk.Label(
            controls, text="Text size:",
            bg="#eef2f7"
        ).grid(row=3, column=0, padx=5, pady=5, sticky="w")

        tk.Scale(
            controls,
            from_=12,
            to=100,
            orient="horizontal",
            variable=self.font_size,
            command=self.update_preview,
            bg="#eef2f7",
            highlightthickness=0
        ).grid(row=3, column=1, sticky="ew", padx=8)

        tk.Label(
            controls, text="Opacity:",
            bg="#eef2f7"
        ).grid(row=4, column=0, padx=5, pady=5, sticky="w")

        tk.Scale(
            controls,
            from_=30,
            to=255,
            orient="horizontal",
            variable=self.opacity,
            command=self.update_preview,
            bg="#eef2f7",
            highlightthickness=0
        ).grid(row=4, column=1, sticky="ew", padx=8)

        controls.columnconfigure(1, weight=1)

        self.preview_area = tk.Label(
            self.root,
            text="Your image preview will appear here.",
            bg="white",
            fg="#64748b",
            relief="groove",
            bd=2
        )
        self.preview_area.pack(
            fill="both", expand=True, padx=22, pady=15
        )

        buttons = tk.Frame(self.root, bg="#eef2f7")
        buttons.pack(pady=(0, 18))

        tk.Button(
            buttons,
            text="Preview Watermark",
            command=self.update_preview,
            padx=14,
            pady=8
        ).pack(side="left", padx=6)

        tk.Button(
            buttons,
            text="Save Watermarked Image",
            command=self.save_image,
            bg="#15803d",
            fg="white",
            padx=14,
            pady=8
        ).pack(side="left", padx=6)

    def choose_image(self):
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("All files", "*.*")
            ]
        )

        if not path:
            return

        try:
            with Image.open(path) as image:
                self.original_image = image.convert("RGBA")

            self.image_path = Path(path)
            self.file_label.config(text=self.image_path.name)
            self.update_preview()

        except Exception as error:
            messagebox.showerror(
                "Image Error",
                f"Could not open this image:\n{error}"
            )

    def get_font(self, size):
        # Try common Windows fonts, then use Pillow's default font.
        font_paths = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/calibri.ttf"
        ]

        for font_path in font_paths:
            if Path(font_path).exists():
                try:
                    return ImageFont.truetype(font_path, size)
                except OSError:
                    pass

        return ImageFont.load_default()

    def make_watermarked_image(self):
        if self.original_image is None:
            raise ValueError("Please choose an image first.")

        text = self.watermark_text.get().strip()
        if not text:
            raise ValueError("Please enter watermark text.")

        image = self.original_image.copy()
        draw = ImageDraw.Draw(image)

        size = self.font_size.get()
        font = self.get_font(size)
        padding = max(15, size // 2)

        # Measure the text so it fits at the selected position.
        box = draw.textbbox((0, 0), text, font=font, stroke_width=1)
        text_width = box[2] - box[0]
        text_height = box[3] - box[1]
        width, height = image.size

        positions = {
            "Bottom Right": (
                width - text_width - padding,
                height - text_height - padding
            ),
            "Bottom Left": (
                padding, height - text_height - padding
            ),
            "Top Right": (
                width - text_width - padding, padding
            ),
            "Top Left": (padding, padding),
            "Center": (
                (width - text_width) // 2,
                (height - text_height) // 2
            )
        }

        x, y = positions[self.position.get()]

        # Draw semi-transparent white text with a dark outline.
        draw.text(
            (x, y),
            text,
            font=font,
            fill=(255, 255, 255, self.opacity.get()),
            stroke_width=max(1, size // 20),
            stroke_fill=(0, 0, 0, min(255, self.opacity.get()))
        )

        return image

    def update_preview(self, _event=None):
        if self.original_image is None:
            return

        try:
            watermarked = self.make_watermarked_image()
            preview = watermarked.copy()
            preview.thumbnail((780, 330))

            # Tkinter needs ImageTk to display a Pillow image.
            self.preview_photo = ImageTk.PhotoImage(preview)
            self.preview_area.config(
                image=self.preview_photo,
                text=""
            )

        except (ValueError, KeyError) as error:
            self.preview_area.config(image="", text=str(error))

    def save_image(self):
        if self.original_image is None or self.image_path is None:
            messagebox.showwarning(
                "No Image",
                "Please choose an image first."
            )
            return

        try:
            watermarked = self.make_watermarked_image()

            default_name = (
                f"{self.image_path.stem}_watermarked.png"
            )

            save_path = filedialog.asksaveasfilename(
                title="Save watermarked image",
                initialfile=default_name,
                defaultextension=".png",
                filetypes=[
                    ("PNG image", "*.png"),
                    ("JPEG image", "*.jpg"),
                    ("WebP image", "*.webp")
                ]
            )

            if not save_path:
                return

            extension = Path(save_path).suffix.lower()

            # JPEG does not support transparency.
            if extension in (".jpg", ".jpeg"):
                watermarked = watermarked.convert("RGB")

            watermarked.save(save_path)

            messagebox.showinfo(
                "Success",
                f"Watermarked image saved successfully:\n{save_path}"
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the image:\n{error}"
            )


if __name__ == "__main__":
    window = tk.Tk()
    app = WatermarkApp(window)
    window.mainloop()
