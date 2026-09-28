import { ttsApi } from '../../api/tts'
import { toast } from '../ui/Toast'

interface Props {
  soundCount: number
  volume: number
}

export function Header({ soundCount, volume }: Props) {
  const handleShutdown = async () => {
    if (!confirm('shut down the server?')) return
    try {
      await ttsApi.shutdown()
      toast('shutting down...', 'success')
    } catch {
      toast('shutdown failed', 'error')
    }
  }

  return (
    <div className="header">
      <div className="header-top">
        <h1>▸ SOUNDPAD</h1>
        <button className="btn shutdown-btn" onClick={handleShutdown}>shutdown</button>
      </div>
      <div className="sub">
        sounds: {soundCount} │ volume: {volume}% │{' '}
        <kbd>/</kbd> search │ <kbd>Esc</kbd> stop
      </div>
    </div>
  )
}
