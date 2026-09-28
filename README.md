# Soundpad

Cross-platform soundboard with a web UI. Play sound effects through your speakers, mix them into your microphone input (Linux/PipeWire), and use text-to-speech — all from a browser.

## Features

- **Sound library** — upload, rename, delete, and search audio files (mp3, wav, ogg, flac, opus, m4a)
- **One-click playback** — tap a pad to play instantly
- **Mic mixing** — on Linux with PipeWire, route sounds into a virtual microphone so other apps hear them alongside your voice
- **Text-to-speech** — type text and play it through your speakers (powered by gTTS)
- **Keyboard hotkeys** — bind any sound to a key combo
- **Customizable UI** — pick an accent color, adjust volume up to 200%
- **Background / tray mode** — daemonize the server and control it remotely
- **Cross-platform audio** — auto-detects `pw-play`, `paplay`, `afplay`, `ffplay`, or PowerShell

## Tech stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | Python, FastAPI, Uvicorn        |
| Frontend | React 19, TypeScript, Vite      |
| Audio    | PipeWire / PulseAudio / afplay / ffplay |
| TTS      | gTTS (Google Text-to-Speech)    |

## Quick start

### Prerequisites

- Python 3.12+
- Node.js 20+ (only for frontend development)
- An audio backend: `pw-play` (PipeWire), `paplay` (PulseAudio), `afplay` (macOS), or `ffplay` (FFmpeg)

### Install & run

```bash
# Clone the repo
git clone https://github.com/Kvazar-213452/Sound.git
cd Sound

# Install Python dependencies
pip install fastapi uvicorn gtts

# Initialize config and directories
python main.py --init

# Start the server
python main.py
```

Open **http://localhost:5000** in your browser.

### Frontend development

```bash
cd frontend
npm install
npm run dev      # Vite dev server with hot reload (proxies API to :5000)
npm run build    # Build to ../static/
```

## Usage

```
python main.py                # start on http://0.0.0.0:5000
python main.py --port 8080    # custom port
python main.py --mic          # enable mic mixing (Linux/PipeWire)
python main.py --tray         # run in background (daemonize)
python main.py --stop         # stop the background process
python main.py --status       # check if a background process is running
python main.py --dev          # verbose debug logging
python main.py --init         # create config.json and sounds/ directory
```

## Project structure

```
├── main.py                  # CLI entry point
├── config.json              # Runtime configuration
├── sounds/                  # Sound files (gitignored)
├── app/
│   ├── server.py            # FastAPI app factory
│   ├── config.py            # Config loading / saving
│   ├── models/              # Pydantic request/response models
│   ├── routes/
│   │   ├── sounds.py        # /api/sounds, /api/play, /api/upload, ...
│   │   ├── tts_routes.py    # /api/tts
│   │   └── config_routes.py # /api/config
│   └── services/
│       ├── player.py        # Cross-platform audio playback
│       ├── sound_library.py # Sound file management
│       ├── tts.py           # Text-to-speech via gTTS
│       ├── mic_mixer.py     # PipeWire/PulseAudio virtual mic
│       └── daemon.py        # PID file, daemonize, tray mode
├── frontend/                # React + TypeScript + Vite
│   └── src/
│       ├── App.tsx
│       ├── components/      # UI components (pads, settings, upload, TTS, ...)
│       ├── hooks/           # React hooks (useSounds, useConfig, useKeyboard, ...)
│       ├── api/             # API client functions
│       └── types/           # TypeScript type definitions
└── static/                  # Built frontend (served by FastAPI)
```

## API

| Method | Endpoint       | Description               |
|--------|----------------|---------------------------|
| GET    | `/api/sounds`  | List all sounds           |
| POST   | `/api/play`    | Play a sound              |
| POST   | `/api/stop`    | Stop playback             |
| POST   | `/api/upload`  | Upload a sound file       |
| POST   | `/api/delete`  | Delete a sound            |
| POST   | `/api/rename`  | Rename a sound            |
| POST   | `/api/tts`     | Text-to-speech            |
| GET    | `/api/config`  | Get current configuration |
| POST   | `/api/config`  | Update configuration      |
| POST   | `/api/shutdown`| Shut down the server      |

## License

MIT
