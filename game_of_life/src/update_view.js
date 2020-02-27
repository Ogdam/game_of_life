///////////////////////////////// CREATE EMPTY GAME /////////////////////////////////
function create_empty_basic_view(){
    var base_view = "";
    for (i=0;i<50;i++){
      base_view += "<tr>";
      for (j=0;j<50;j++){
        base_view += "<td class='case'></td>";
      }
      base_view += "</tr>";
    }
    $("#game_of_life").empty();
    $("#game_of_life").append(base_view);
}

///////////////////////////////// LOAD GAME BOARD //////////////////////////////
function get_game(){
  var matrice = [];
  var cpt = -1;
  $("#game_of_life").children().each(function(){
    cpt +=1;
    matrice.push([]);
    $(this).children().each(function() {
      if($(this).hasClass("alive")){
        matrice[cpt].push(1);}
      else{
        matrice[cpt].push(0);}
    });
  });
  return matrice
}

/////////////////////////////////////////////

function lets_play(){
  base_matrice = get_game
}

function main_control(){
  create_empty_basic_view();
}

///////////////////////////////// CONTROL /////////////////////////////////
$( document ).ready(function() {
  main_control();

  $('td.case').on("click", function(){
    $(this).toggleClass("alive");
  });


  $('#start').on("click", function(){
    console.log("let the game crash");
    lets_play();
  });

  $('#stop').on("click", function(){
    console.log("do something else");
  });

});
