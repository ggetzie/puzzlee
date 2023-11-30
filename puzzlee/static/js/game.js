var squaresRemaining = 12;
var gameOver = false;
var canReveal = true;
const allArtists = JSON.parse(
  document.getElementById("all-artists").textContent
);
const answer = parseInt(document.getElementById("answer").textContent);
const artworkTitle = document.getElementById("artwork-title").textContent;
const clickASquare = "Click a square to reveal a portion of the artwork";
const enterAGuess =
  "Start typing the name of an artist and click Guess to make a guess";

function setupGrid() {
  const grid = document.getElementById("grid");
  let messages = document.getElementById("messages");
  messages.textContent = clickASquare;
  for (let i = 0; i < 12; i++) {
    let square = document.createElement("div");
    square.classList.add("grid-square");
    square.onclick = function () {
      if (!canReveal) {
        return;
      }
      this.style.visibility = "hidden";
      canReveal = false;
      let guessInput = document.getElementById("guess-input");
      guessInput.disabled = false;
      guessInput.focus();
      let button = document.getElementById("guess-button");
      button.disabled = false;
      squaresRemaining--;
      messages.textContent = enterAGuess;
    };
    grid.appendChild(square);
  }
}

function addGuessToList(guess) {
  let guessList = document.getElementById("guess-list");
  let guessItem = document.createElement("li");
  guessItem.classList.add("list-group-item", "failed-guess");
  guessItem.textContent = guess;
  guessList.appendChild(guessItem);
}

function getAnswerName() {
  for (let artist in allArtists) {
    if (allArtists[artist] == answer) {
      return artist;
    }
  }
  return "";
}

function endGame() {
  let painting = document.getElementById("painting");
  painting.style.display = "block";
  painting.style.visibility = "visible";
  let grid = document.getElementById("grid");
  grid.style.display = "none";
  gameOver = true;
  document.getElementById("guess-input").value = "";
  document.getElementById("guess-input").disabled = true;
  document.getElementById("guess-button").disabled = true;
}

function win() {
  endGame();
  messages = document.getElementById("messages");
  messages.textContent = `You won! It's ${artworkTitle} by ${getAnswerName()}`;
}

function lose() {
  endGame();
  messages = document.getElementById("messages");
  messages.textContent = `You lost! It's ${artworkTitle} by ${getAnswerName()}`;
}

function checkGuess() {
  if (gameOver) {
    return;
  }
  let guessInput = document.getElementById("guess-input");
  let guess = guessInput.value;

  console.log(allArtists);

  let guess_id = allArtists[guess];
  console.log("guess_id: %d", guess_id);
  console.log("answer: %d", answer);
  if (guess_id == answer) {
    console.log("winner");
    win();
  } else {
    addGuessToList(guess);
    canReveal = true;
    document.getElementById("guess-input").value = "";
    document.getElementById("guess-input").disabled = true;
    document.getElementById("guess-button").disabled = true;
    if (squaresRemaining == 0) {
      lose();
    } else {
      let messages = document.getElementById("messages");
      messages.textContent = clickASquare;
    }
    document.getElementById("guess-header").textContent =
      "Guesses Remaining: " + squaresRemaining;
  }
}

window.onload = function () {
  let painting = document.getElementById("painting");
  if (painting) {
    painting.style.display = "none";
    setupGrid();
    setTimeout(function () {
      painting.style.display = "block";
    }, 1000);
  }
};
