# Stage 2 — Motor IDs

Every DYNAMIXEL motor leaves the factory as **ID 1 at 57600 baud**. Seventeen motors all
answering to "1" on one cable just talk over each other, so each motor gets its own ID
**before** they are chained together — one motor at a time, with nothing mechanical attached.
The tool that does it runs on your robot's Pi, so the Pi is set up first.

---

## 1. Set up the Pi — your workbench computer

*Software lead, with the mentor. This can happen on day one while Stage 1 prints.*

You need: the Raspberry Pi 5 and its **official 27 W power supply**, the Active Cooler, the SD
card the mentor prepared for your robot, a monitor and a micro-HDMI cable, a USB keyboard and
mouse, your team's USB stick, and the school wifi (the install downloads packages).

1. Press the **Active Cooler** onto the Pi (its two push-pins go into the holes beside the
   processor) and plug its fan lead into the socket marked FAN.
2. SD card in, then monitor (the HDMI port nearest the power socket), keyboard and mouse, and
   power last. The Pi starts to the desktop.
3. Connect to the wifi from the network icon at the top right, if the mentor hasn't already.
4. Plug in the USB stick. In the file manager, copy `software/reachy-software.tar.gz` from the
   stick into your **home folder**.
5. Open a **Terminal** (the black icon on the top bar) and install the software:
   ```bash
   tar -xzf reachy-software.tar.gz
   cd ~/reachy
   bash scripts/provision_pi.sh
   ```
   It takes several minutes and ends with **Done**. It installs the robot software, the motor
   tools, and the permission to use the motor adapter.
6. **Restart the Pi** (`sudo reboot`). That permission only takes effect after a restart.

**From here on, every command in this book is typed in a Terminal on the Pi, starting in the
`reachy` folder.** A new Terminal starts in your home folder, so type `cd ~/reachy` first.

---

## 2. Motor power on the bench (mentor)

The motors take **5 V** from the **U2D2 Power Hub**. On this robot the Power Hub is fed by a
converter that turns the 12 V power brick into 5 V ([Appendix B](MENTOR_SETUP.md) says how the
mentor wires it).

1. **Mentor:** with no motor plugged in, switch on and measure the Power Hub's input with a meter.
   It must read **about 5.0 V** (4.9–5.1). If it reads 12, stop: something is wired wrong, and 12 V
   destroys every motor it reaches.
2. Switch the Power Hub **off**. Plug the U2D2 into one of the Pi's USB ports, and connect the
   U2D2 to the Power Hub with the short 3-pin cable.

---

## 3. The ID map — the same on every robot

| ID | Motor | Model number the scripts print | Where it goes |
|---:|---|---:|---|
| 1 | XL330-**M077** | 1190 | Left antenna (the robot's own left) |
| 2 | XL330-**M077** | 1190 | Right antenna |
| 3 | **XC330**-M288 (metal case) | 1240 | Body turn, in the base |
| 4–9 | XL330-**M288** | 1200 | The six head motors |
| 14 | XL330-M288 | 1200 | **Right** arm — shoulder pitch (in the shoulder housing) |
| 15 | XL330-M288 | 1200 | **Right** arm — shoulder roll (on the fork, above the shoulder) |
| 16 | XL330-M288 | 1200 | **Right** arm — elbow (lying flat in the upper arm) |
| 17 | XL330-M288 | 1200 | **Right** arm — wrist (in the forearm) |
| 18–21 | XL330-M288 | 1200 | **Left** arm — the same order: pitch, roll, elbow, wrist |

All seventeen run at **1 Mbps** (1 000 000 baud). IDs 10–13 are not used. The software expects
exactly this map.

**The arm order matters.** The software reads the first ID of each arm as the shoulder pitch,
the next as the roll, and so on. On Ollie two shoulder motors went in the wrong places, and the
pitch slider moved the roll joint. Labelling every motor with its job now is what prevents that.

The head and the arms use the **same** motor, the XL330-M288. The two antenna motors (M077) look
identical but are weaker and faster, and the body-turn motor is the one with the metal case.
Check the model number the script prints every time.

---

## 4. Give each motor its ID

1. **Power Hub off.** Plug **one** motor into the Power Hub. Switch on — the motor's LED
   blinks once.
2. Give it its ID and the fast baud rate. For a head motor that will be ID 4:
   ```bash
   cd ~/reachy
   .venv/bin/python scripts/set_id.py --new-id 4 --new-baud 1000000
   ```
   The script refuses if it sees more than one motor, which is the point. It prints the motor's
   model number — check it against the table.
3. **Power off.** Stick a tape label on the motor with robot, ID and job: `R3 · 4 · head`,
   `R3 · 14 · R shoulder pitch`, `R3 · 21 · L wrist`. Unplug it.
4. Repeat for all seventeen: the two **M077** motors (1190) get IDs 1 and 2, the **XC330**
   (1240) gets ID 3, six M288 get 4–9, and eight M288 get 14–21.

## 5. All together, and a health check

5. Chain all seventeen together in any order (power off while you plug), switch on, and scan:
   ```bash
   .venv/bin/python scripts/scan_dynamixel.py
   ```
   You should see **exactly seventeen** motors at 1000000: 1–2 = XL330-M077, 3 = XC330-M288,
   4–9 and 14–21 = XL330-M288. **Count them.** Two motors accidentally given the same ID look
   exactly like one working motor, and nothing else will tell you.
6. **Does every motor actually reach where it's told?**
   ```bash
   .venv/bin/python scripts/nudge_diag.py --ids 1,2,3,4,5,6,7,8,9,14,15,16,17,18,19,20,21
   .venv/bin/python scripts/motor_status.py
   ```
   `nudge_diag` moves each motor a few degrees each way **and reads it back**. A motor whose
   position doesn't change while it draws only a **little** current has a broken gear — the motor
   spins but the output doesn't; Ollie had one straight out of the box. (A **lot** of current and
   no movement means something is blocking it.) `motor_status` should show **no hardware
   error**, about **5 V**, and room temperature on every motor.

### ✅ Checkpoint 2

- [ ] The Pi starts to the desktop, and `cd ~/reachy` works in a Terminal
- [ ] 5 V measured at the Power Hub before any motor was connected
- [ ] The scan shows exactly 17 motors — 1–9 and 14–21 — all at 1000000, the right model on each ID
- [ ] `nudge_diag` shows every motor reaching its targets in both directions
- [ ] Every motor labelled with robot number, ID and job

**If a motor won't show up:** power the motors off and on (a motor that stalled can go silent
until its power is cycled), reseat its cable, try it alone, try
`scan_dynamixel.py --all-bauds`. If its LED lights but it never answers, check the cable is in a
3-pin **TTL** port on the hub. Trust the ID the scan reports over the sticker — stickers get
shuffled.
