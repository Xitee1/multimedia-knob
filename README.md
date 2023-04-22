# multimedia-knob
Use the Raspberry Pi Pico as an multimedia knob to control your PC volume and play/pause music.

As a base of the code, I use [Raspberry Pi Pico - CircuitPython volume knob](https://gist.github.com/maxmacstn/805991009e9302977f694e5b17a62b73).
### Whats better in this version?
With the original version, the knob very often stopped working. Either after sleep, reboot or just randomly while the PC is on. With this version it works very reliably. I haven't had to re-plug the Pi Pico for a few weeks now and it survived all sleep/wake cycles and reboots.

#### Some more little improvements:
- Prints messages only when in debug mode
- Does not automatically mount the storage. This cleans up the file explorer a bit. To edit the code, hold the button down while plugging the Pi in. If that does not work you can alternatively type the commands mentioned in the program at the top.

### Other noteworthy things
As I don't use it, I have removed the mode changing function. I haven't fully removed it but only removed the function to change the "currentMode". It should be rather easy to add it back in.

## How to use it:
Note: As I no longer know the exact procedure this might not work the way I explain it here.
1. Plug in the Pi Pico
1.1. (Somehow install CircuitPython? I don't know if it comes pre installed.) 
2. Copy-paste all files from the "pico" folder of this repo on the Pi Pico by using the normal file explorer (The Pico will shop up as storage device).
3. This should be everything.

I know this is an pretty bad explanaition.. maybe I'll update it someday.
