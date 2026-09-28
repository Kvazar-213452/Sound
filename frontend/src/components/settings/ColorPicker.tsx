const PRESETS = [
  { color: '#39ff14', label: 'acid green' },
  { color: '#00ff00', label: 'green' },
  { color: '#44aaff', label: 'blue' },
  { color: '#ff5555', label: 'red' },
  { color: '#ffaa00', label: 'orange' },
  { color: '#cc88ff', label: 'purple' },
  { color: '#00ffff', label: 'cyan' },
]

function expandHex(hex: string): string {
  if (hex.length === 4) {
    return `#${hex[1]}${hex[1]}${hex[2]}${hex[2]}${hex[3]}${hex[3]}`
  }
  return hex
}

interface Props {
  value: string
  onChange: (color: string) => void
}

export function ColorPicker({ value, onChange }: Props) {
  return (
    <div className="color-options">
      {PRESETS.map(p => (
        <div
          key={p.color}
          className={`color-dot ${value === p.color ? 'active' : ''}`}
          style={{ background: p.color }}
          title={p.label}
          onClick={() => onChange(p.color)}
        />
      ))}
      <input
        type="color"
        className="color-custom"
        value={expandHex(value)}
        title="custom"
        onChange={e => onChange(e.target.value)}
      />
    </div>
  )
}
