
import requests
from bs4 import BeautifulSoup

url = "https://www.empireonline.com/movies/features/best-movies-2/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# ویب صفحے سے فلموں کے عنوان تلاش کریں
movie_elements = soup.select("h3")

movies = []

for element in movie_elements:
    title = element.get_text(strip=True)

    if title and title not in movies:
        movies.append(title)

# فلموں کی فہرست الٹی ترتیب میں لکھیں
movies.reverse()

with open("movies.txt", "w", encoding="utf-8") as file:
    for movie in movies:
        file.write(movie + "\n")

print(f"Total movies found: {len(movies)}")
print("Movie list saved in movies.txt")
