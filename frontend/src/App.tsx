import { useCallback, useState } from 'react'
import type { Tab } from './types'
import { useSounds } from './hooks/useSounds'
import { useConfig } from './hooks/useConfig'
import { useTheme } from './hooks/useTheme'
import { useKeyboard } from './hooks/useKeyboard'
import { Header } from './components/layout/Header'
import { Tabs } from './components/layout/Tabs'
import { Prompt } from './components/layout/Prompt'
import { SoundsTab } from './components/sounds/SoundsTab'
import { UploadTab } from './components/upload/UploadTab'
import { BindsTab } from './components/binds/BindsTab'
import { SettingsTab } from './components/settings/SettingsTab'
import { TtsTab } from './components/tts/TtsTab'
import { ToastContainer } from './components/ui/Toast'

export default function App() {
  const [tab, setTab] = useState<Tab>('sounds')
  const { sounds, playing, load, play, stop } = useSounds()
  const { config, update } = useConfig()

  useTheme(config.accent_color)
  useKeyboard({ hotkeys: config.hotkeys, onPlay: play, onStop: stop, setTab })

  const handleUploadDone = useCallback(() => { load(); setTab('sounds') }, [load])
  const handleBindsUpdate = useCallback((hotkeys: Record<string, string>) => { update({ hotkeys }) }, [update])

  return (
    <div className="shell">
      <Header soundCount={sounds.length} volume={Math.round(config.volume * 100)} />
      <Tabs active={tab} onChange={setTab} />

      <div className="panel">
        {tab === 'sounds' && (
          <SoundsTab sounds={sounds} playing={playing} hotkeys={config.hotkeys} onPlay={play} onStop={stop} onReload={load} />
        )}
        {tab === 'upload' && <UploadTab onDone={handleUploadDone} />}
        {tab === 'binds' && <BindsTab sounds={sounds} hotkeys={config.hotkeys} onUpdate={handleBindsUpdate} />}
        {tab === 'tts' && <TtsTab />}
        {tab === 'settings' && <SettingsTab config={config} onUpdate={update} />}
      </div>

      <Prompt />
      <ToastContainer />
    </div>
  )
}
