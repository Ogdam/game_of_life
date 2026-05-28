function neighbor_number(x, y, matrice){
  var neighbor = 0;
  for(var i=x-1; i<=x+1; i++){
    for(var j=y-1; j<=y+1; j++){
        if ((i == x && j == y) || i < 0 || j < 0 || i >= matrice.length || j >= matrice[i].length)
          continue;
        neighbor += matrice[i][j];
    }
  }
  return neighbor;
}

function test_if_resurect_or_not(alive, neighbor){
  if (alive == 1 && (neighbor == 2 || neighbor == 3))
    return 1;
  else if (alive == 1 )
    return 0;

  if (alive == 0 && neighbor == 3)
    return 1;
  else if (alive == 0)
    return 0;
}

function update_matrice(base_matrice){
  var new_matrice = base_matrice.map(function(arr) {
    return arr.slice();
  });
  for(var i=0;i<new_matrice.length;i++){
    for(var j=0;j<new_matrice[i].length;j++){
      new_matrice[i][j] = test_if_resurect_or_not(base_matrice[i][j], neighbor_number(i, j, base_matrice));
    }
  }
  return new_matrice;
}
