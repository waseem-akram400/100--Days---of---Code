from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

folder = Path(__file__).resolve().parent
html_file = folder / "dino_game.html"

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Offline Dinosaur Game</title>
<style>
body { font-family: Arial; text-align: center; margin-top: 40px; }
canvas { border-bottom: 2px solid #555; max-width: 95%; }
</style>
</head>
<body>
<h2>Offline Dinosaur Game</h2>
<p>Python Selenium will control the dinosaur.</p>
<canvas id="game" width="800" height="220"></canvas>
<p id="score">Score: 0</p>
<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const state = { dinoY: 170, velocity: 0, obstacleX: 800,
                jumping: false, over: false, score: 0 };
window.gameState = state;

function jump() {
  if (!state.jumping && !state.over) {
    state.velocity = -12;
    state.jumping = true;
  }
}
document.addEventListener("keydown", e => {
  if (e.code === "Space") {
    e.preventDefault();
    jump();
  }
});

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#333";
  ctx.fillRect(50, state.dinoY, 25, 30);
  ctx.fillRect(66, state.dinoY - 10, 15, 15);
  ctx.fillRect(55, state.dinoY + 20, 6, 10);
  ctx.fillRect(70, state.dinoY + 20, 6, 10);

  ctx.fillStyle = "green";
  ctx.fillRect(state.obstacleX, 175, 20, 25);
  ctx.fillRect(state.obstacleX + 5, 165, 10, 15);

  ctx.fillStyle = "#333";
  ctx.fillText("Space = Jump", 650, 25);

  if (!state.over) {
    state.obstacleX -= 5;
    if (state.obstacleX < -30) {
      state.obstacleX = 800 + Math.random() * 250;
      state.score++;
      document.getElementById("score").textContent =
        "Score: " + state.score;
    }

    state.dinoY += state.velocity;
    state.velocity += 0.6;
    if (state.dinoY >= 170) {
      state.dinoY = 170;
      state.velocity = 0;
      state.jumping = false;
    }

    if (state.obstacleX < 78 && state.obstacleX > 35 &&
        state.dinoY > 140) {
      state.over = true;
      ctx.fillStyle = "red";
      ctx.font = "28px Arial";
      ctx.fillText("Game Over - restart the program", 180, 100);
    }
  }
  requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
"""

html_file.write_text(html, encoding="utf-8")
print("Opening the offline Dinosaur Game...")

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get(html_file.as_uri())
    body = driver.find_element(By.TAG_NAME, "body")
    print("Automation started. Press Ctrl+C in Terminal to stop.")

    while True:
        state = driver.execute_script("return window.gameState")
        if state is None or state["over"]:
            print("Game ended. Run the program again to restart.")
            break

        if 35 < state["obstacleX"] < 125 and not state["jumping"]:
            body.send_keys(Keys.SPACE)

        time.sleep(0.025)

except KeyboardInterrupt:
    print("Automation stopped.")

finally:
    driver.quit()
    print("Browser closed.")
