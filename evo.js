"use strict";

var output_text = document.getElementById("output");
var output = []; // this will be a list containing lists.
var state = []; // this will be
output = treeTest(output, current);

function treeTest(output, current) {
  var current_tick = [];
  console.log(current);
  while (current.length < 5) {
    treeTest(current.push(1));
    treeTest(current.push(2));
  }
  return current;
}


function treeTest(current_game){
    var current_tick = [];
    // run game logic

    while notDone(current_game){
        while actionsExist(current_game){ // if a non-wait action exists.
            current_tick.push(1); // you can always wait, but sometimes it's deliberate (and not useless)
            ifCanDo2(current_tick.push(2));
            ifCanDo3(current_tick.push(3));
        }
        //if(current_tick === [])
        //    current_tick.push(1); // if the tick had no possible actions, put in a 1 for wait.
        treeTest(current_game.push(current_tick));

    }
    
}

function isDone(current_state){

}

function notDone(current_game){
    if(!goalReached(current_game))
}

function actionsExist(current_game){

    if(CanDo(current_game, 1))
        return true;
    else if(CanDo(current_game, 1))
        return true;
    else if(CanDo(current_game, 1))
        return true;
    else if(CanDo(current_game, 1))
        return true;
    else
        return false;
}
*/
