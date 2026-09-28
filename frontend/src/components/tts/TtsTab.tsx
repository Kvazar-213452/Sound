import { useState } from 'react'
import { ttsApi } from '../../api/tts'
import { toast } from '../ui/Toast'

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'uk', label: 'Ukrainian' },
  { code: 'de', label: 'German' },
  { code: 'fr', label: 'French' },
  { code: 'es', label: 'Spanish' },
  { code: 'ja', label: 'Japanese' },
  { code: 'ko', label: 'Korean' },
  { code: 'zh-CN', label: 'Chinese' },
]

export function TtsTab() {
  const [text, setText] = useState('')
  const [lang, setLang] = useState('en')
  const [loading, setLoading] = useState(false)

  const speak = async () => {
    if (!text.trim()) return
    setLoading(true)
    try {
      await ttsApi.speak(text.trim(), lang)
      toast('speaking', 'success')
    } catch {
      toast('TTS error', 'error')
    }
    setLoading(false)
  }

  return (
    <>
      <div className="tts-header">text-to-speech</div>
      <div className="tts-controls">
        <select className="tts-lang" value={lang} onChange={e => setLang(e.target.value)}>
          {LANGUAGES.map(l => (
            <option key={l.code} value={l.code}>{l.label}</option>
          ))}
        </select>
      </div>
      <textarea
        className="tts-input"
        placeholder="type text to speak..."
        value={text}
        onChange={e => setText(e.target.value)}
        rows={6}
      />
      <div className="tts-actions">
        <span className="tts-count">{text.length}/5000</span>
        <button className="btn accent" onClick={speak} disabled={loading || !text.trim()}>
          {loading ? 'generating...' : '▸ SPEAK'}
        </button>
      </div>
    </>
  )
}
