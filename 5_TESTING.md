# Stage 5 — Testing

Three tests, in this order: the **acceptance test** (is the robot sound?), the **Code Lab** (can
you program it with blocks and JavaScript?) and **VR control** (can a headset drive it?). A
robot is done when every box in this chapter is ticked.

> **One program on the motors at a time.** The robot software owns the motors. Before running
> **any** motor script from the troubleshooting table: `sudo systemctl stop reachy`, check
> `pgrep -af 'app\.main|app\.serve'` prints nothing, and `sudo systemctl start reachy` afterwards.

**Finding the robot's address.** The Code Lab and VR are opened from other devices, which need the
Pi's address on the wifi. In a Terminal on the Pi, `hostname -I` prints it — the first number,
like `192.168.1.57`. The robot's pages are at `http://<that address>:8080`.

---

## 1. Acceptance test

The whole team, with the checklist.

- [ ] **Start-up:** unplug everything, plug it back in. The robot comes back on its own in under
      a minute; the head goes level; the face shows eyes (tap once for sound)
- [ ] **Gestures** from the console: 👋 Greet · 😌 Nod · 📡 Wiggle · 👀 Look · 🎉 Celebrate · 🤔 Think —
      smooth, no clicking, no binding, no rod pops
- [ ] **Antennae** move, and "left" is the robot's own left
- [ ] **Body turn** — 90° each way and back, with the arms and every cable coming along cleanly
- [ ] **Arms:** after a restart, on `/limbs`, tick **Drive the real arm** and **🎯 Test live
      robot** passes on both sides — without anyone capturing a zero again
- [ ] **Voice:** it says a line out of the phone; the mute switch on the console silences it
- [ ] **30-minute run**, used the way it will be at a demo: every few minutes play a few
      gestures, turn the body, and run a Code Lab show with the arms in it (section 2).
      Afterwards (software stopped) `motor_status.py` shows no hardware errors, no motor is too
      hot to hold a finger on, and the mentor checks the 5 V converter is warm, not hot
- [ ] Everything labelled; the team log up to date (ID map, calibration date, who did what)

---

## 2. The Code Lab — Blockly and JavaScript

The **Code Lab** is where students program the robot. You build a show out of blocks (Blockly)
or write it in JavaScript, watch a cartoon of the robot act it out, and then run it on the real
robot. The two are connected: **Show me the code** turns your blocks into the JavaScript that does
the same thing, so you can move from blocks to typing without starting over.

The block palette isn't stored in the page — it's **built from the robot's own list** of
gestures, moods, head poses and arm poses. So if the blocks appear, the page is talking to your
robot. (The page calls every robot "Ollie": it's the same software.)

Open **`http://<robot's address>:8080/lab`** — on the Pi itself it's
`http://localhost:8080/lab`, but try it from a laptop, tablet or phone on the same wifi too,
because that's where students will use it.

1. **Blocks.** The **🧩 Blocks** tab shows a palette of robot blocks. Drag in a **say** block and
   type "Hello", then a **do a** block and pick **celebrate** from its list. Press **▶ Run**.
   *What Ollie will do* shows the robot's script, and the preview plays it. Open the lists on
   the **do a** and **look** blocks: those are your robot's own gestures and head poses.
2. **Blocks → JavaScript.** Press **Show me the code**. The **⌨️ JavaScript** tab opens with your
   blocks written as code, something like `ollie.say('Hello');` and
   `ollie.gesture('celebrate');`. Change the words in the code and press **▶ Run** — the preview
   says the new words. That's the connection working in both directions: blocks became code,
   and the code runs.
3. **A loop.** Press **↺ Example**. It loads a program with a `for` loop that waves the antennae
   three times — the kind of thing blocks can't say as neatly. Press **▶ Run** and watch the
   preview.
4. **On the real robot.** Press **🤖 Run on Ollie**. The real robot performs the program: the
   voice from the phone, the antennae, the arm wave. **⏹ Stop** stops it. **⤼ Step** runs one
   action at a time — the way to find which line does what.
5. **Send it in.** Type a name for the show and your name, and press **Submit**. It goes to the
   teacher's review list on the console, where a teacher can approve it.

### ✅ Checkpoint 5.2

- [ ] The block palette appears (the page reached the robot)
- [ ] **Show me the code** turns blocks into JavaScript, and an edited program runs in the preview
- [ ] **🤖 Run on Ollie** makes the real robot perform it, and **⏹ Stop** stops it
- [ ] It works from a second device on the same wifi, not just the Pi

**If it goes wrong:** no blocks at all means the page couldn't load the block library or reach
the robot — check the address, and tell the mentor (the software may be missing its Blockly
file). If *Run on Ollie* says an arm isn't ready, that side isn't live and zeroed — go back to
Stage 4, step 4.

---

## 3. VR control

With a **Meta Quest** headset you can stand next to a life-size virtual copy of your robot. Hold a
**grip** button and the *real* robot's head follows your head. Hold the **trigger** and talk,
and your voice comes out of the robot. The virtual robot moves along with the real one.

⚠️ **Two people.** The person in the headset can't see the real robot. The second person watches
the robot the whole time, with a hand near the Power Hub's switch, and says out loud what it's
doing. VR never moves the arms — on purpose, for exactly this reason.

### Once per robot: a certificate (mentor)

A headset only allows VR on a **secure (https)** page, so the robot needs a certificate:

```bash
cd ~/reachy
bash scripts/make_cert.sh
.venv/bin/pip install numpy
sudo systemctl restart reachy
```

(`numpy` is what lets the robot change your voice into its character voices. Without it, VR
still works, and you hear your own voice.) Two things change, and both are expected:

- **The robot's pages move to `https://<address>:8080`.** Browsers warn that the certificate
  isn't trusted, because it's home-made. Press **Advanced → Proceed** (on the Pi, the console is
  now `https://localhost:8080`).
- **Plain http moves to port 8081.** The phone face uses plain http, so its home-screen icon
  stops working. On the phone, open `http://<address>:8081/eyes?audio=1`, tap once, choose **Add
  to Home screen** again, and delete the old icon.

### The test

1. Put the Quest on the **same wifi as the robot**. In the Quest's browser, open
   `https://<address>:8080/vr` and press **Advanced → Proceed**.
2. The flat page shows your robot in 3D, moving when the real one moves.
3. Press **Enter VR**. **Allow the microphone** when asked — it can only ask here, before you go
   in.
4. The robot stands in front of you, life-size.
5. **Head.** Hold a **grip** button and turn your head to your right — the real robot turns to
   *its* right. Nod — it nods. Tilt — it tilts. Let go — it stops where it is. The watcher says
   whether each direction matched. If one is backwards, write down which, and tell the mentor
   (it's one setting to flip).
6. **Voice.** Hold the **trigger** and talk. When you let go, your voice — shifted towards a
   robot character — comes out of the phone in the robot's head. The waveform under the **Voice**
   button moves while you talk; if it stays flat, the microphone isn't reaching the page.
   Pressing **Voice** changes the character.
7. **Control panel.** On the panel beside you, the **Motion** tab has the gestures: press one and
   the real robot does it.
8. **Exit VR** — the button above your eyeline, apart from everything else.

### ✅ Checkpoint 5.3

- [ ] The virtual robot appears and follows the real one
- [ ] Holding a grip drives the real head, in the right direction on all three axes, and letting
      go stops it
- [ ] Your voice comes out of the robot, and the waveform moves when you talk
- [ ] A gesture from the panel plays on the real robot
- [ ] The phone face was re-added on port 8081 and still speaks

---

## 4. When something goes wrong

Stop the robot software before running any of these scripts (the box at the top of this
chapter).

| Symptom | Most likely | Do this |
|---|---|---|
| A motor missing from the scan | Cable, or it stalled and latched a fault | Power the motors off and on (not just the Pi). Reseat its cable. `motor_status.py --reboot <id>` clears a latched fault |
| All motors vanish when one part is plugged in | A wiring fault in that part | Unplug it; test it alone with a known-good cable |
| A motor "moves" but the joint doesn't | Broken gear | `nudge_diag.py --ids <id>` — low current and no movement = gear; high current = something blocking it |
| Head stiff, won't reach its angles | Neck ball-joint screws too tight | Back each one off until it swivels freely |
| A rod pops off a ball | Ball undersize, or a reused rod | Measure the ball; print a fresh rod |
| Head sags when the motors are off | Gravity — normal | Nothing |
| `calibrate show` says `(defaults)` | The calibration file is missing or has a typo | Don't run `home`. Fix the file or copy it back from the USB stick |
| An arm joint moves the wrong way | Its belt pulley went on the other way round | Press that joint's **⇄** on `/limbs` |
| A slider moves the wrong joint | Two arm motors are in each other's places | On `/limbs`, with **Drive the real arm** unticked, pick the right motor in that joint's **id** list, then **🔍 Find motors** (Stage 4, step 4) |
| **🎯 Test live robot** stops on one joint | A slipped belt or a stuck joint | Limp the arm, check the belt is on its teeth and the joint turns by hand |
| An arm clicks or jumps under load | The belt is skipping teeth | Tension it (the pitch motor has a pry window); check the cover isn't forcing a pulley |
| An arm is dead after a restart | `ARM_START` isn't set, or its zero is missing | `ARM_START=both` in `.env`; `/health` → `arms` says which |
| The U2D2 disappears from USB | Loose USB cable | Reseat it; it comes back |
| The robot lists motors that aren't there | It lists what it found when it started | Restart the robot software after any rewiring |
| The face is silent | The phone hasn't been tapped since its page reloaded | Amber eyes = tap the face once |
| The phone can't open the robot's page | Not on the same wifi — or the wifi blocks devices talking to each other (many school networks do) | Check the wifi name on both; if it's the school network, ask the mentor |
| Code Lab: no blocks | The page didn't reach the robot, or the Blockly file is missing | Check the address; tell the mentor |
| VR: no **Enter VR** button, or it says VR isn't available | The page isn't on https | Use `https://…:8080/vr` (the certificate step) |
| VR: the head turns the wrong way | One axis is mirrored | Note which axis; the mentor flips it ([Appendix B](MENTOR_SETUP.md)) |
| Body turns but stops short or creeps | A tired or damaged yaw motor | `nudge_diag.py --ids 3` |
