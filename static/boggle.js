"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board 
 * Takes in board array of array containing letters and fills table
 * with letters.
*/

function displayBoard(board) {
  $table.empty();
  let $tbody = $('<tbody>');

  for (let row of board) {
    let $row = $('<tr>');
    for (let letter of row) {
      let $cell = $(`<td>${letter}</td>`);
      $row.append($cell);
    }
    $tbody.append($row);
  }
  $table.append($tbody);
}

/** Handle submit word
 * Send request to API to see if word is legal. 
 * Call show result with API's response. 
*/

async function handleWordSubmit(evt) {
  evt.preventDefault();
  $message.empty();
  let word = $wordInput.val().toUpperCase();

  let data = { "word": word, "gameId": gameId}
  let response = await axios.post("api/score-word", data);
  let result = response.data.result;

  show_result(result, word);

  $form.trigger('reset');
}

/** Show the result in the DOM. 
 * If the result is "ok", append the word to the word list. 
 * If the play is invalid, show invalid word message. */ 

function show_result(result, word) {
  if (result === "not-word") {
    $message.text('Not a valid word!');
  } else if (result === "not-on-board") {
    $message.text('Not a word on the board!');
  } else {
    $playedWords.append(`<li>${word}</li>`);
  }
}

$form.on('submit', handleWordSubmit);

start();