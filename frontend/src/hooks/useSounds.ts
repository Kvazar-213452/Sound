import { useCallback, useEffect, useState } from 'react'
import { soundsApi } from '../api/sounds'
import type { Sound } from '../types'

export function useSounds() {
  const [sounds, setSounds] = useState<Sound[]>([])
  const [playing, setPlaying] = useState<string | null>(null)

  const load = useCallback(async () => {
    setSounds(await soundsApi.list())
  }, [])

  useEffect(() => { load() }, [load])

  const play = useCallback(async (file: string) => {
    setPlaying(file)
    await soundsApi.play(file)
  }, [])

  const stop = useCallback(async () => {
    setPlaying(null)
    await soundsApi.stop()
  }, [])

  return { sounds, playing, load, play, stop }
}
