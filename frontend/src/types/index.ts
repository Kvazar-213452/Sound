export interface Sound {
  id: string
  name: string
  file: string
  ext: string
}

export interface Config {
  volume: number
  play_to_speakers: boolean
  mic_mode: boolean
  accent_color: string
  hotkeys: Record<string, string>
  tray_mode: boolean
}

export type Tab = 'sounds' | 'upload' | 'binds' | 'tts' | 'settings'
