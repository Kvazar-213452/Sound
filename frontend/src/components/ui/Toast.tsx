import { useEffect, useState } from 'react'

interface Item {
  id: number
  msg: string
  type: '' | 'success' | 'error'
}

let _push: (msg: string, type?: Item['type']) => void = () => {}

export function toast(msg: string, type: Item['type'] = '') {
  _push(msg, type)
}

export function ToastContainer() {
  const [items, setItems] = useState<Item[]>([])

  useEffect(() => {
    _push = (msg, type = '') => {
      const id = Date.now() + Math.random()
      setItems(prev => [...prev, { id, msg, type }])
      setTimeout(() => setItems(prev => prev.filter(t => t.id !== id)), 2500)
    }
  }, [])

  return (
    <div className="toast-container">
      {items.map(t => (
        <div key={t.id} className={`toast ${t.type}`}>{t.msg}</div>
      ))}
    </div>
  )
}
