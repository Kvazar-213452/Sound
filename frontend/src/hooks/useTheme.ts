import { useEffect } from 'react'

function hexToRgb(hex: string): [number, number, number] {
  let h = hex.replace('#', '')
  if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2]
  return [parseInt(h.substring(0,2),16), parseInt(h.substring(2,4),16), parseInt(h.substring(4,6),16)]
}

export function useTheme(accentColor: string) {
  useEffect(() => {
    const [r, g, b] = hexToRgb(accentColor)
    const root = document.documentElement
    root.style.setProperty('--accent', accentColor)
    root.style.setProperty('--accent2', `rgb(${Math.round(r*0.7)},${Math.round(g*0.7)},${Math.round(b*0.7)})`)
    root.style.setProperty('--glow', `rgba(${r},${g},${b},0.12)`)
  }, [accentColor])
}
