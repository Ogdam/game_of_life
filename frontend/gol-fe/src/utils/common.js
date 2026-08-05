export function cantor_calcul(x, y) {
  return ((x + y) * (x + y + 1)) / 2 + y
}

export function getCellColor(current_gen, birth) {
  const age = current_gen - birth

  const t = Math.min(age / 60, 1)

  const g = 255 - Math.floor(255 * t) // chute forte
  const b = 120 - Math.floor(120 * t) // disparition complète

  return (0 << 16) + (g << 8) + b
}
