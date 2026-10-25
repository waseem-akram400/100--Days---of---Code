import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import csv
import threading


def scrape_website():
    url = url_entry.get().strip()

    if not url:
        messagebox.showwarning("Missing URL", "Please enter a website URL.")
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    if not parsed.netloc:
        messagebox.showerror("Invalid URL", "Please enter a valid website URL.")
        return

    scrape_button.config(state="disabled")
    status_label.config(text="Fetching webpage...")
    results_text.delete("1.0", tk.END)

    def worker():
        try:
            response = requests.get(
                url,
                headers={
                    "User-Agent": "EducationalWebScraper/1.0"
                },
                timeout=15
            )
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type.lower():
                raise ValueError("The URL did not return an HTML webpage.")

            soup = BeautifulSoup(response.text, "html.parser")

            # Remove elements that usually do not contain page content.
            for element in soup(["script", "style", "noscript"]):
                element.decompose()

            page_title = (
                soup.title.get_text(" ", strip=True)
                if soup.title else "No page title"
            )

            headings = []
            for tag in soup.find_all(["h1", "h2", "h3"]):
                heading = tag.get_text(" ", strip=True)
                if heading:
                    headings.append({
                        "type": tag.name,
                        "text": heading
                    })

            links = []
            for tag in soup.find_all("a", href=True):
                link_text = tag.get_text(" ", strip=True)
                full_link = requests.compat.urljoin(url, tag["href"])

                if full_link.startswith(("http://", "https://")):
                    links.append({
                        "text": link_text,
                        "url": full_link
                    })

            data = {
                "url": url,
                "title": page_title,
                "headings": headings,
                "links": links
            }

            root.after(0, lambda: show_results(data))

        except Exception as error:
            message = str(error)
            root.after(0, lambda: show_error(message))

    threading.Thread(target=worker, daemon=True).start()


def show_results(data):
    global scraped_data
    scraped_data = data

    results_text.insert(tk.END, f"Page title: {data['title']}\n")
    results_text.insert(tk.END, f"URL: {data['url']}\n\n")

    results_text.insert(tk.END, "HEADINGS\n")
    results_text.insert(tk.END, "-" * 45 + "\n")

    if data["headings"]:
        for item in data["headings"]:
            results_text.insert(
                tk.END, f"{item['type'].upper()}: {item['text']}\n"
            )
    else:
        results_text.insert(tk.END, "No headings found.\n")

    results_text.insert(tk.END, "\nLINKS\n")
    results_text.insert(tk.END, "-" * 45 + "\n")

    for item in data["links"][:200]:
        label = item["text"] or "(No link text)"
        results_text.insert(tk.END, f"{label}\n{item['url']}\n\n")

    status_label.config(
        text=f"Done: {len(data['headings'])} headings, "
             f"{len(data['links'])} links found."
    )
    save_button.config(state="normal")
    scrape_button.config(state="normal")


def show_error(message):
    status_label.config(text="Scraping failed.")
    scrape_button.config(state="normal")
    messagebox.showerror("Scraping Error", message)


def save_csv():
    if not scraped_data:
        messagebox.showwarning("No data", "Scrape a webpage first.")
        return

    path = filedialog.asksaveasfilename(
        title="Save scraped data",
        defaultextension=".csv",
        initialfile="scraped_data.csv",
        filetypes=[("CSV files", "*.csv")]
    )

    if not path:
        return

    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Page URL", scraped_data["url"]])
            writer.writerow(["Page Title", scraped_data["title"]])
            writer.writerow([])
            writer.writerow(["Heading Type", "Heading Text"])

            for item in scraped_data["headings"]:
                writer.writerow([item["type"], item["text"]])

            writer.writerow([])
            writer.writerow(["Link Text", "Link URL"])

            for item in scraped_data["links"]:
                writer.writerow([item["text"], item["url"]])

        messagebox.showinfo("Saved", f"Data saved successfully:\n{path}")

    except Exception as error:
        messagebox.showerror("Save Error", str(error))


def clear_results():
    global scraped_data
    scraped_data = None
    results_text.delete("1.0", tk.END)
    url_entry.delete(0, tk.END)
    save_button.config(state="disabled")
    status_label.config(text="Ready")


scraped_data = None

root = tk.Tk()
root.title("Day 93 - Custom Web Scraper")
root.geometry("760x650")
root.minsize(600, 500)

tk.Label(
    root,
    text="Custom Web Scraper",
    font=("Arial", 20, "bold")
).pack(pady=(15, 5))

tk.Label(
    root,
    text="Enter a public webpage URL to collect its headings and links."
).pack(pady=5)

url_frame = tk.Frame(root)
url_frame.pack(fill="x", padx=15, pady=10)

url_entry = tk.Entry(url_frame, font=("Arial", 11))
url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
url_entry.insert(0, "https://example.com")

scrape_button = tk.Button(
    url_frame, text="Scrape", command=scrape_website
)
scrape_button.pack(side="left")

results_frame = tk.Frame(root)
results_frame.pack(fill="both", expand=True, padx=15, pady=5)

scrollbar = ttk.Scrollbar(results_frame)
scrollbar.pack(side="right", fill="y")

results_text = tk.Text(
    results_frame,
    wrap="word",
    font=("Consolas", 10),
    yscrollcommand=scrollbar.set
)
results_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=results_text.yview)

button_frame = tk.Frame(root)
button_frame.pack(pady=8)

save_button = tk.Button(
    button_frame,
    text="Save Results to CSV",
    command=save_csv,
    state="disabled"
)
save_button.pack(side="left", padx=5)

tk.Button(
    button_frame, text="Clear", command=clear_results
).pack(side="left", padx=5)

status_label = tk.Label(root, text="Ready", fg="blue")
status_label.pack(pady=(0, 10))

root.mainloop()
