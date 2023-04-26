# multimedia-knob
![image-preview](https://user-images.githubusercontent.com/59659167/234576393-500a1231-701e-4776-b843-6a909da3d1f8.png)

Use the Raspberry Pi Pico as an multimedia knob to control your PC volume and play/pause music.

As a base of the code, I use [Raspberry Pi Pico - CircuitPython volume knob](https://gist.github.com/maxmacstn/805991009e9302977f694e5b17a62b73), made by [maxmacstn](https://gist.github.com/maxmacstn).

### What's better in this version?
With the original version, the knob very often stopped working. Either after sleep, reboot or just randomly while the PC is on. With this version it works very reliably. I haven't had to re-plug the Pi Pico for a few weeks now and it survived all sleep/wake cycles and reboots.

_Note: When opening Thonny on the PC it might stop working again. Close Thonny (or better restart you PC), then plug out, wait 5-10 secs until Windows realizes it, then plug it back in._

#### Some more little improvements:
- Prints messages only when in debug mode
- Does not automatically mount the storage. This cleans up the file explorer a bit. To edit the code, hold the button down while plugging the Pi in. If that does not work you can alternatively type the commands mentioned in the program at the top.

### Other noteworthy things
As I don't use it, I have removed the mode changing function. I haven't fully removed it but only removed the function to change the "currentMode". It should be rather easy to add it back in.

## How to use it:
1. Download the [CircuitPython UF2 file](https://circuitpython.org/board/raspberry_pi_pico/)
2. Plug in the Pi Pico while holding the bootload button
3. The Pico mounts as storage device on you PC
4. Copy the UF2 file in the root directory of the Pico
5. The Pico will install CircuitPython and then automatically reboot
6. After reboot, you should see a storage device called "CIRCUITPY"
7. Copy all files of the "pico" directory on github into that storage device
8. Re-plug the Pi and try if it works

You can also watch [this Tutorial](https://www.youtube.com/watch?v=M6K8vwzZrYs). It is also made by the original creator of this program (GH: [maxmacstn](https://gist.github.com/maxmacstn) / YT: [magi](https://www.youtube.com/@magichannel)).

## 3D print case
The original creator of this script also made [this case](https://www.thingiverse.com/thing:4799088) for it.
