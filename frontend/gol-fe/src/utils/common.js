export function cantor_calcul(x, y) {
  return ((x + y) * (x + y + 1)) / 2 + y
}

const BIRTH_COLOR = { r: 0x00, g: 0x79, b: 0x59 } // #007959, naissance de la cellule
const AGED_COLOR = { r: 0x00, g: 0x5a, b: 0x5c } // #005a5c, cellule âgée d'au moins MAX_AGE_TICKS ticks
const MAX_AGE_TICKS = 100

export function getCellColor(current_gen, birth) {
  const age = current_gen - birth
  const t = Math.min(age / MAX_AGE_TICKS, 1)

  const r = Math.round(BIRTH_COLOR.r + (AGED_COLOR.r - BIRTH_COLOR.r) * t)
  const g = Math.round(BIRTH_COLOR.g + (AGED_COLOR.g - BIRTH_COLOR.g) * t)
  const b = Math.round(BIRTH_COLOR.b + (AGED_COLOR.b - BIRTH_COLOR.b) * t)

  return (r << 16) + (g << 8) + b
}
