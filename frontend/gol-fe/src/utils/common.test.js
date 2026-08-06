import { describe, it, expect } from 'vitest'
import { cantor_calcul, getCellColor } from './common'

describe('cantor_calcul', () => {
  it('produces a unique value for a given pair of coordinates', () => {
    expect(cantor_calcul(0, 0)).toBe(0)
    expect(cantor_calcul(1, 2)).toBe(8)
  })

  it('produces different values for different coordinate pairs', () => {
    const a = cantor_calcul(1, 2)
    const b = cantor_calcul(2, 1)
    expect(a).not.toBe(b)
  })
})

describe('getCellColor', () => {
  it('returns the birth color when the cell just appeared', () => {
    expect(getCellColor(10, 10)).toBe(0x007959)
  })

  it('returns the aged color once the cell reaches the max age', () => {
    expect(getCellColor(100, 0)).toBe(0x005a5c)
  })

  it('clamps age beyond the max age threshold to the aged color', () => {
    expect(getCellColor(500, 0)).toBe(0x005a5c)
  })

  it('interpolates the color between birth and aged colors', () => {
    const color = getCellColor(50, 0)
    expect(color).toBe(0x6a5b)
    expect(color).toBeLessThan(0x007959)
    expect(color).toBeGreaterThan(0x005a5c)
  })
})
