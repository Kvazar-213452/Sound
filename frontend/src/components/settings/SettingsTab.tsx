import type { Config } from '../../types'
import { Toggle } from '../ui/Toggle'
import { ColorPicker } from './ColorPicker'

interface Props {
  config: Config
  onUpdate: (patch: Partial<Config>) => void
}

export function SettingsTab({ config, onUpdate }: Props) {
  const vol = Math.round(config.volume * 100)

  return (
    <>
      <div className="settings-group">
        <div className="settings-group-title">audio</div>
        <div className="setting">
          <div className="setting-label">
            volume<span>playback volume</span>
          </div>
          <div className="setting-right">
            <input
              type="range"
              className="slider"
              min={0} max={200} value={vol}
              onChange={e => onUpdate({ volume: Number(e.target.value) / 100 })}
            />
            <span className="vol-val">{vol}%</span>
          </div>
        </div>
        <div className="setting">
          <div className="setting-label">
            play_to_speakers<span>play sound to speakers</span>
          </div>
          <Toggle on={config.play_to_speakers} onChange={v => onUpdate({ play_to_speakers: v })} />
        </div>
        <div className="setting">
          <div className="setting-label">
            mic_mode<span>mix sound into microphone (Linux/PipeWire)</span>
          </div>
          <Toggle on={config.mic_mode} onChange={v => onUpdate({ mic_mode: v })} />
        </div>
      </div>

      <div className="settings-group">
        <div className="settings-group-title">system</div>
        <div className="setting">
          <div className="setting-label">
            tray_mode<span>run in background (--tray)</span>
          </div>
          <Toggle on={config.tray_mode} onChange={v => onUpdate({ tray_mode: v })} />
        </div>
      </div>

      <div className="settings-group">
        <div className="settings-group-title">theme</div>
        <div className="setting">
          <div className="setting-label">
            accent_color<span>UI accent color</span>
          </div>
          <ColorPicker value={config.accent_color} onChange={c => onUpdate({ accent_color: c })} />
        </div>
      </div>
    </>
  )
}
