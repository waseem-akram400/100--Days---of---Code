import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from collections import Counter


def generate_palette():
    file_path = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")
        ]
    )

    if not file_path:
        return

    try:
        image = Image.open(file_path).convert("RGB")
        preview = image.copy()
        preview.thumbnail((350, 180))

        photo = ImageTk.PhotoImage(preview)
        image_label.config(image=photo, text="")
        image_label.image = photo

        # Reduce the image to 8 representative colours.
        small_image = image.copy()
        small_image.thumbnail((150, 150))
        quantized = small_image.quantize(colors=8)

        palette = quantized.getpalette()
        colour_counts = Counter(quantized.getdata())
        colours = []

        for index, count in colour_counts.most_common(8):
            red = palette[index * 3]
            green = palette[index * 3 + 1]
            blue = palette[index * 3 + 2]
            hex_code = f"#{red:02X}{green:02X}{blue:02X}"
            colours.append((hex_code, count))

        # Clear the previous palette.
        for widget in palette_frame.winfo_children():
            widget.destroy()

        for hex_code, count in colours:
            row = tk.Frame(palette_frame, pady=3)
            row.pack(fill="x", padx=10)

            swatch = tk.Label(
                row, bg=hex_code, width=8, height=2,
                relief="solid", borderwidth=1
            )
            swatch.pack(side="left", padx=(0, 10))

            colour_label = tk.Label(
                row, text=hex_code, font=("Arial", 11, "bold")
            )
            colour_label.pack(side="left")

            copy_button = tk.Button(
                row,
                text="Copy",
                command=lambda colour=hex_code: copy_colour(colour)
            )
            copy_button.pack(side="right")

        save_button.config(
            state="normal",
            command=lambda data=colours: save_palette(data)
        )
        status_label.config(text=f"Found {len(colours)} colours.")

    except Exception as error:
        messagebox.showerror("Image Error", str(error))


def copy_colour(colour):
    root.clipboard_clear()
    root.clipboard_append(colour)
    root.update()
    status_label.config(text=f"{colour} copied!")


def save_palette(colours):
    file_path = filedialog.asksaveasfilename(
        title="Save colour palette",
        defaultextension=".txt",
        initialfile="colour_palette.txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not file_path:
        return

    with open(file_path, "w", encoding="utf-8") as file:
        file.write("Image Colour Palette\n\n")
        for colour, count in colours:
            file.write(f"{colour} - {count} pixels\n")

    messagebox.showinfo("Saved", f"Palette saved to:\n{file_path}")


root = tk.Tk()
root.title("Day 92 - Image Colour Palette Generator")
root.geometry("500x650")
root.minsize(450, 550)

tk.Label(
    root,
    text="Image Colour Palette Generator",
    font=("Arial", 17, "bold")
).pack(pady=(15, 8))

tk.Label(
    root,
    text="Choose an image to discover its main colours."
).pack(pady=4)

tk.Button(
    root,
    text="Choose Image",
    command=generate_palette,
    font=("Arial", 11),
    padx=12,
    pady=6
).pack(pady=10)

image_label = tk.Label(root, text="No image selected")
image_label.pack(pady=5)

tk.Label(
    root, text="Colour Palette",
    font=("Arial", 13, "bold")
).pack(pady=(10, 5))

palette_frame = tk.Frame(root)
palette_frame.pack(fill="x", padx=15)

save_button = tk.Button(
    root, text="Save Palette to Text File",
    state="disabled"
)
save_button.pack(pady=12)

status_label = tk.Label(root, text="Ready", fg="blue")
status_label.pack(pady=5)

root.mainloop()
