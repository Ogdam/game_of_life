function neighbor_number(x, y, matrice){
  next = 0
  for(var i=x-1; i<=x+1; i++){
    for(var j=y-1; j<=y+1; j++){
      try{
        if (i == x && j == y)
          continue;
        next += matrice[i][j]? Number.isInteger(matrice[i][j]): 0;
      }catch(e){}
    }
  }
  return next;
}


function test_if_resurect_or_not(value, next){
  if (value == 1 && (next == 2 || next == 3))
    return 1;
  if (value == 1 && (next < 2 || next > 3))
    return 0;
  if (value == 0 && next != 3)
    return 0;
  if (value == 0 && next == 3)
    return 1;
}

function update_matrice(matrice){
  for(var i=0;  i<matrice.length; i++){
    for(var j=0; j<matrice[i].length; j++){
      new_matrice[i][j] = test_if_resurect_or_not(matrice[i][j], neighbor_number(i, j, matrice))
    }
  }
  new_matrice;
  return new_matrice
}
