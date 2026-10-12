from pathlib import Path
import webbrowser
html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Favourite Movies</title>
</head>
<body>
    <h1>The Best Movies According to Me</h1>
    <h2>My Top 3 Movies of All Time</h2>
    <hr>
    <h3>1. 3 Idiots</h3>
    <p>This movie teaches us to follow our passion.</p>
    <h3>2. The Lion King</h3>
    <p>This is an enjoyable animated movie.</p>
    <h3>3. Home Alone</h3>
    <p>This movie is funny and entertaining.</p>
</body>
</html>
"""
file_path = Path(__file__).with_name("index.html")
file_path.write_text(html_code, encoding="utf-8")
webbrowser.open(file_path.resolve().as_uri())
print("Day 41 Movie Ranking website tayyar hai!")
