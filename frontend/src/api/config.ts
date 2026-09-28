import type { Config } from '../types'
import { get, post } from './client'

export const configApi = {
  get: () => get<Config>('/api/config'),
  set: (update: Partial<Config>) => post<Config>('/api/config', update),
}
