import { useCallback, useEffect, useState } from 'react'
import { configApi } from '../api/config'
import type { Config } from '../types'

const DEFAULTS: Config = {
  volume: 0.8,
  play_to_speakers: true,
  mic_mode: false,
  accent_color: '#39ff14',
  hotkeys: {},
  tray_mode: false,
}

export function useConfig() {
  const [config, setConfig] = useState<Config>(DEFAULTS)

  useEffect(() => {
    configApi.get().then(setConfig)
  }, [])

  const update = useCallback(async (patch: Partial<Config>) => {
    const c = await configApi.set(patch)
    setConfig(c)
  }, [])

  return { config, update }
}
