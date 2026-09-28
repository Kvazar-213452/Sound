import type { Sound } from '../types'
import { get, post, upload } from './client'

export const soundsApi = {
  list: () => get<Sound[]>('/api/sounds'),
  play: (file: string) => post('/api/play', { file }),
  stop: () => post('/api/stop'),
  upload: (file: File) => upload('/api/upload', file),
  delete: (file: string) => post('/api/delete', { file }),
  rename: (file: string, name: string) => post('/api/rename', { file, name }),
}
