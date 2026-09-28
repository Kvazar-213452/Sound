import { useCallback, useEffect } from 'react'
import type { Tab } from '../types'

interface Opts {
  hotkeys: Record<string, string>
  onPlay: (file: string) => void
  onStop: () => void
  setTab: (tab: Tab) => void
}

export function useKeyboard({ hotkeys, onPlay, onStop, setTab }: Opts) {
  const handler = useCallback((e: KeyboardEvent) => {
    const el = e.target as HTMLElement
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') return

    if (e.key === 'Escape') { onStop(); return }

    if (e.key === '/' && !e.ctrlKey && !e.altKey) {
      e.preventDefault()
      setTab('sounds')
      setTimeout(() => document.getElementById('search-input')?.focus(), 50)
      return
    }

    if (hotkeys[e.code]) {
      e.preventDefault()
      onPlay(hotkeys[e.code])
    }
  }, [hotkeys, onPlay, onStop, setTab])

  useEffect(() => {
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [handler])
}
