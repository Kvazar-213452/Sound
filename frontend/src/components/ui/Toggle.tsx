interface Props {
  on: boolean
  onChange: (value: boolean) => void
}

export function Toggle({ on, onChange }: Props) {
  return (
    <button
      className={`toggle ${on ? 'on' : ''}`}
      onClick={() => onChange(!on)}
    />
  )
}
