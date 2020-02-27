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

    $('td.case').on("click", function(){
      $(this).toggleClass("alive");
      console.log(1);
    });
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
  return matrice;
}

/////////////////////////////////////////////


function lets_play(matrice){
    setTimeout(function() {
        matrice = update_matrice(matrice);
        draw_new_board(matrice);
        if (Play == true)
          lets_play(matrice);
    }, 300);
}

function draw_new_board(matrice){
    var base_view = "";
    for (i=0;i<50;i++){
      base_view += "<tr>";
      for (j=0;j<50;j++){
        if (matrice[i][j] == 0){
          base_view += "<td class='case'></td>";}
          else {base_view += "<td class='case alive'></td>";}
      }
      base_view += "</tr>";
    }
    $("#game_of_life").empty();
    $("#game_of_life").append(base_view);

    $('td.case').on("click", function(){
      $(this).toggleClass("alive");
      console.log(1);
    });
}

///////////////////////////////// CONTROL /////////////////////////////////

var Play = false;

$( document ).ready(function() {
  create_empty_basic_view();

  $('td.case').on("click", function(){
    $(this).toggleClass("alive");
    console.log(1);
  });


  $('#start').on("click", function(){
    console.log("let the game crash");
    Play = true
    matrice = get_game();
    lets_play(matrice.slice());
  });

  $('#stop').on("click", function(){
    Play = false
  });

  $('#restart').on("click", function(){
    Play = false;
    create_empty_basic_view();
  });

});
