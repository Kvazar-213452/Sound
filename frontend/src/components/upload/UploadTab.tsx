import { useCallback, useRef, useState } from 'react'
import { soundsApi } from '../../api/sounds'
import { toast } from '../ui/Toast'

interface Props {
  onDone: () => void
}

export function UploadTab({ onDone }: Props) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const upload = useCallback(async (files: FileList) => {
    for (const f of Array.from(files)) {
      try {
        const res = await soundsApi.upload(f)
        toast(`uploaded: ${res.file}`, 'success')
      } catch {
        toast(`error: ${f.name}`, 'error')
      }
    }
    onDone()
  }, [onDone])

  return (
    <>
      <div
        className={`upload-zone ${dragging ? 'drag' : ''}`}
        onClick={() => inputRef.current?.click()}
        onDragOver={e => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={e => { e.preventDefault(); setDragging(false); upload(e.dataTransfer.files) }}
      >
        <div className="icon">↑</div>
        <p>drag and drop files or click to browse</p>
        <p className="small">.mp3 .wav .ogg .flac .opus .m4a</p>
      </div>
      <input
        ref={inputRef}
        type="file"
        accept=".mp3,.wav,.ogg,.flac,.opus,.m4a"
        multiple
        hidden
        onChange={e => e.target.files && upload(e.target.files)}
      />
    </>
  )
}
