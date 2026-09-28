import { post } from './client'

export const ttsApi = {
  speak: (text: string, lang: string = 'en') => post('/api/tts', { text, lang }),
  shutdown: () => post('/api/shutdown'),
}
