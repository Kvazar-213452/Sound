import type { Tab } from '../../types'

const TABS: Tab[] = ['sounds', 'upload', 'binds', 'tts', 'settings']

interface Props {
  active: Tab
  onChange: (tab: Tab) => void
}

export function Tabs({ active, onChange }: Props) {
  return (
    <div className="tabs">
      {TABS.map(t => (
        <button
          key={t}
          className={`tab ${active === t ? 'active' : ''}`}
          onClick={() => onChange(t)}
        >
          {t}
        </button>
      ))}
    </div>
  )
}
