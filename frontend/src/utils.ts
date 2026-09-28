export function formatKey(key: string): string {
  return key
    .replace('Key', '')
    .replace('Digit', '')
    .replace('Numpad', 'Num')
    .replace('ArrowUp', '↑')
    .replace('ArrowDown', '↓')
    .replace('ArrowLeft', '←')
    .replace('ArrowRight', '→')
}

export function getBindForFile(hotkeys: Record<string, string>, file: string): string | null {
  for (const [key, f] of Object.entries(hotkeys)) {
    if (f === file) return key
  }
  return null
}
