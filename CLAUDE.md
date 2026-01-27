# CLAUDE.md

This file provides context for AI assistants working on this repository.

## Project Overview

**multimedia-knob** is a CircuitPython project that turns a Raspberry Pi Pico into a USB multimedia knob. It reads a rotary encoder via GPIO pins and sends USB HID consumer control commands to the host PC for volume control and media playback.

Current version: **2.1**

> **Note:** The maintainer recommends [luckkyboy/multimedia-knob](https://github.com/luckkyboy/multimedia-knob) as the actively developed fork. This repository is unlikely to receive further updates.

## Technology Stack

- **Runtime:** CircuitPython (Python 3 variant for microcontrollers)
- **Hardware:** Raspberry Pi Pico + rotary encoder with push button
- **Protocol:** USB HID (Human Interface Device)
- **Library:** Adafruit HID (bundled in `pico/lib/`)
- **IDE:** JetBrains (`.idea/` present, gitignored)

## Repository Structure

```
multimedia-knob/
├── .gitignore              # Ignores .idea/
├── README.md               # User-facing documentation
├── CLAUDE.md               # This file (AI assistant context)
└── pico/                   # All device code lives here
    ├── boot.py             # Runs first on power-up; disables USB drive mount
    ├── code.py             # Main application (rotary encoder + HID control)
    └── lib/
        └── adafruit_hid/   # Bundled Adafruit HID library (MIT license)
            ├── __init__.py
            ├── consumer_control.py
            ├── consumer_control_code.py
            ├── keyboard.py
            ├── keycode.py
            ├── keyboard_layout_base.py
            ├── keyboard_layout_us.py
            └── mouse.py
```

## Key Files

### `pico/boot.py`
Startup script that calls `storage.disable_usb_drive()` to prevent the Pico from mounting as a USB drive during normal use. Users hold the encoder button while plugging in to re-enable the drive for code editing.

### `pico/code.py`
The main application. This is the primary file you will modify. Key aspects:

- **GPIO pins:** CLK=GP4, DT=GP3, SW=GP2 (rotary encoder clock, data, switch)
- **HID devices:** `ConsumerControl` for media keys, `Keyboard` imported but not actively used
- **Functions:**
  - `cw()` / `ccw()` — handle clockwise/counter-clockwise rotation (volume up/down)
  - `short_press()` — play/pause on button tap
  - `long_press()` — currently a no-op (placeholder for future use)
  - `reset_keyboard(force)` — re-initializes HID devices on error (key reliability feature)
  - `loop()` — main event loop: reads encoder state, detects rotation direction, handles button presses
  - `millis()` — returns current time in milliseconds
  - `log(message)` — debug-controlled print wrapper

### `pico/lib/adafruit_hid/`
Bundled third-party library. Do not modify these files. The library provides USB HID device classes for consumer control, keyboard, mouse, and keycode mappings.

## Hardware Interaction

### Rotary Encoder Wiring
| Encoder Pin | Pico GPIO | Purpose |
|-------------|-----------|---------|
| CLK | GP4 | Clock signal for rotation detection |
| DT | GP3 | Data signal for direction detection |
| SW | GP2 | Push button (pulled up, active low) |

### Rotation Direction Detection
When CLK goes low: if DT differs from CLK, rotation is clockwise; if equal, counter-clockwise.

### Button Detection
- Short press: button released within 1 second
- Long press: button held longer than 1 second
- 200ms debounce delay after initial press detection

### USB HID Commands Sent
| Action | HID Code |
|--------|----------|
| Rotate clockwise | `VOLUME_INCREMENT` (0xE9) |
| Rotate counter-clockwise | `VOLUME_DECREMENT` (0xEA) |
| Short press | `PLAY_PAUSE` (0xCD) |

## Code Conventions

### Naming
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `CLK_PIN`, `DT_PIN`, `SW_PIN`)
- **Functions:** `snake_case` (e.g., `reset_keyboard`, `short_press`, `long_press`)
- **Variables:** mostly `snake_case`, though some legacy `camelCase` remains (e.g., `rotateDelay`, `currentMode`, `totalModes`)

### Patterns
- **Error recovery:** All HID operations are wrapped in try/except blocks. On failure, `reset_keyboard(True)` reinitializes the HID devices after a 1-second delay. This is the key reliability improvement in v2.1.
- **Debug logging:** Use `log()` instead of `print()` for debug output. The `debug` flag (line 22 of code.py) controls whether messages are printed.
- **GPIO init:** Input pins use `digitalio.DigitalInOut` with `Direction.INPUT`. The button pin additionally has `Pull.UP`.
- **Main loop resilience:** The outermost `while True` loop in `__main__` has its own try/except to ensure the device keeps running regardless of errors.

### Style
- No type annotations (CircuitPython has limited support)
- String formatting uses `.format()` (no f-strings in CircuitPython)
- Comments are inline `#` style
- No docstrings on functions

## Development Workflow

### Prerequisites
1. A Raspberry Pi Pico flashed with CircuitPython firmware (UF2 from [circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico/))
2. A rotary encoder wired to GP2/GP3/GP4

### Deploying Code to the Device
1. Hold the encoder button while plugging in the Pico (mounts the filesystem)
2. Copy all files from `pico/` to the root of the `CIRCUITPY` drive
3. Unplug and re-plug the Pico to start running

### Editing Workflow
- The USB drive is disabled by default (`boot.py`). To edit files on the device, hold the button while connecting.
- Alternatively, use the CircuitPython REPL: `import storage; storage.remount("/", readonly=False)`
- **Warning:** Opening Thonny IDE on the PC may interfere with the device. Close Thonny and re-plug if this happens.

### No Build Step
CircuitPython interprets Python files directly. There is no compilation, build system, package manager, or test framework.

### No Package Manager
All dependencies are bundled in `pico/lib/`. There is no `requirements.txt`, `setup.py`, or `pyproject.toml`. To update the Adafruit HID library, download a new version from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) and replace the files in `pico/lib/adafruit_hid/`.

## Important Notes for AI Assistants

1. **Do not modify files in `pico/lib/adafruit_hid/`** — these are vendored third-party library files.
2. **CircuitPython constraints apply:**
   - No f-strings; use `.format()` for string formatting
   - Limited standard library (no `os`, `sys`, `pathlib`, etc.)
   - Available built-in modules: `board`, `digitalio`, `time`, `storage`, `usb_hid`
   - Memory is very constrained on the Pico; keep code minimal
3. **The `boot.py` file runs before `code.py`** and is critical for device behavior at startup. Changes to `boot.py` require re-plugging the device to take effect.
4. **The mode system (`currentMode`, `totalModes`) is vestigial.** Mode switching was intentionally removed in v2.1. The variables remain but only mode 0 (volume control) is active.
5. **The `keyboard` and `Keyboard` import exist for potential future use** but are not actively sending keystrokes. Mouse support is commented out.
6. **Testing is manual only** — there are no automated tests. Verify changes by deploying to a physical Pico and testing the knob/button behavior.
7. **The `debug` flag** on line 22 of `code.py` controls logging verbosity. Set to `True` during development, `False` for production.
