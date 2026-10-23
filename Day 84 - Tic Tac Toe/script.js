// Day 84 - Tic Tac Toe game logic

// Each position represents one square on the board.
let board = Array(9).fill("");
let currentPlayer = "X";
let gameActive = true;

// Winning combinations: rows, columns and diagonals.
const winningCombinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
];

let scores = { X: 0, O: 0 };

// Find HTML elements we need to update.
const cells = document.querySelectorAll(".cell");
const statusText = document.getElementById("status");
const xScore = document.getElementById("x-score");
const oScore = document.getElementById("o-score");
const xCard = document.getElementById("x-card");
const oCard = document.getElementById("o-card");
const restartButton = document.getElementById("restart");
const resetScoresButton = document.getElementById("reset-scores");

// Listen for clicks on every square.
cells.forEach((cell) => {
    cell.addEventListener("click", handleCellClick);
});

restartButton.addEventListener("click", restartGame);
resetScoresButton.addEventListener("click", resetScores);

function handleCellClick(event) {
    const cell = event.currentTarget;
    const index = Number(cell.dataset.index);

    // Do nothing if the game has ended or the square is occupied.
    if (!gameActive || board[index] !== "") {
        return;
    }

    // Save the move and show it on the board.
    board[index] = currentPlayer;
    cell.textContent = currentPlayer;
    cell.classList.add(currentPlayer.toLowerCase());
    cell.disabled = true;

    // Check whether this move wins the game.
    const winningLine = getWinningLine();

    if (winningLine) {
        finishGame(winningLine);
        return;
    }

    // If no squares are empty, the game is a draw.
    if (board.every((square) => square !== "")) {
        gameActive = false;
        statusText.textContent = "It's a draw!";
        return;
    }

    // Switch to the other player.
    currentPlayer = currentPlayer === "X" ? "O" : "X";
    updateTurnDisplay();
}

function getWinningLine() {
    return winningCombinations.find((combination) => {
        const [a, b, c] = combination;

        return (
            board[a] !== "" &&
            board[a] === board[b] &&
            board[a] === board[c]
        );
    });
}

function finishGame(winningLine) {
    gameActive = false;
    statusText.textContent = `Player ${currentPlayer} wins!`;

    // Highlight the three winning squares.
    winningLine.forEach((index) => {
        cells[index].classList.add("winner");
    });

    // Update the winner's score.
    scores[currentPlayer] += 1;
    updateScores();
    updateTurnDisplay();
}

function updateTurnDisplay() {
    xCard.classList.toggle("active", currentPlayer === "X" && gameActive);
    oCard.classList.toggle("active", currentPlayer === "O" && gameActive);
}

function updateScores() {
    xScore.textContent = scores.X;
    oScore.textContent = scores.O;
}

function restartGame() {
    // Clear the board but keep the scores.
    board = Array(9).fill("");
    currentPlayer = "X";
    gameActive = true;

    cells.forEach((cell) => {
        cell.textContent = "";
        cell.disabled = false;
        cell.classList.remove("x", "o", "winner");
    });

    statusText.textContent = "Player X's turn";
    updateTurnDisplay();
}

function resetScores() {
    // Reset both scores and start a fresh round.
    scores = { X: 0, O: 0 };
    updateScores();
    restartGame();
}
