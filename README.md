# 👻 Ghost Horror Mode

A spooky fullscreen experience that transforms your Linux PC into a horror atmosphere before launching **Ekphos**, the TUI markdown editor.

![Platform](https://img.shields.io/badge/platform-Linux%20(X11)-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-purple)

## ✨ Features

- 🩸 **Blood Writing Animation** — "You Are Alone" writes itself with dripping blood effect
- 👁️ **Glowing Purple Eyes** — Fade in, breathe ominously, fade out
- ⌨️ **Keyboard Suppression** — Prevents escape via window manager shortcuts (X11)
- 🔄 **Loop Mode** — Say "no" and return to the darkness
- 🔊 **Sound-Ready** — Architecture prepared for future audio effects

## 📋 Requirements

- **Python 3.8+**
- **X11 Display Server** (i3, KDE on X11, etc.)
- **Ekphos** — TUI markdown editor
- **Terminal Emulator** (kitty, alacritty, foot, wezterm, etc.)

## 🚀 Installation

### 1. Install Ekphos

```bash
# Requires Rust
cargo install ekphos
```

### 2. Clone/Navigate to Ghost Horror

```bash
cd "/home/isaiah/Projects/Ghost Horror"
```

### 3. Run Ghost Horror

```bash
./ghost.sh
```

The first run will automatically:
- Create a Python virtual environment
- Install pygame and python-xlib

## 🎮 Usage

```bash
./ghost.sh
```

### The Experience

```
┌─────────────────────────────────────────────┐
│                                             │
│         ██ BLACK SCREEN ██                  │
│                                             │
│      "You Are Alone" (blood dripping)       │
│                                             │
│              👁️  👁️                         │
│         (purple glowing eyes)               │
│                                             │
│         → Ekphos Launches →                 │
│                                             │
│      "You want to see the light?"           │
│                                             │
│   [yes] → Exit    [no] → Back to darkness   │
│                                             │
└─────────────────────────────────────────────┘
```

### Controls

| Action | Result |
|--------|--------|
| Type `yes` at prompt | Exit gracefully with farewell message |
| Type anything else | "Return to the darkness!" — loops back |
| `Ctrl+C` in terminal | Emergency exit |

## 📁 Project Structure

```
Ghost Horror/
├── ghost.sh              # Launch script (run this!)
├── requirements.txt      # Python dependencies
├── setup.py              # Pip installable package
└── ghost_horror/
    ├── __init__.py
    ├── main.py           # Main orchestration
    ├── display.py        # Fullscreen X11 engine
    ├── effects.py        # Blood text + glowing eyes
    ├── input_grab.py     # Keyboard suppression
    └── ekphos_launcher.py # Terminal detection + launch
```

## ⚙️ Configuration

Currently hardcoded, but easy to modify in `effects.py`:

```python
PURPLE_GLOW = (138, 43, 226)  # Eye color
BLOOD_RED = (139, 0, 0)       # Text color
```

## 🛣️ Roadmap

- [ ] **Wayland Support** — Full keyboard suppression on Wayland
- [ ] **Sound Effects** — Eerie ambient audio
- [ ] **Config File** — Customizable colors, timing, messages
- [ ] **More Horror Elements** — Additional animations and effects

## 🐛 Troubleshooting

### "Ekphos not found"
```bash
cargo install ekphos
```

### "No terminal found"
Make sure you have a terminal emulator installed (kitty, alacritty, foot, etc.)

### Keyboard shortcuts still work
- Make sure you're running on **X11**, not Wayland
- Check: `echo $XDG_SESSION_TYPE` should output `x11`

### Emergency Exit
Press `Ctrl+C` in the original terminal where you launched `ghost.sh`

## 📜 License

MIT License — Use it, modify it, scare your friends with it.

---

*"You Are Alone..."* 👻
