# Stage 4 — Software installation

The robot software went onto the Pi in Stage 2. This stage turns it into **your** robot: its
name and settings, a first start, the head's limits and the arms' zeros, starting by itself,
and the phone face. Everything is done on the Pi, with its monitor and keyboard.

| Step | What | Who |
|---|---|---|
| [1](#1-name-and-settings) | The robot's name and settings | Software lead |
| [2](#2-first-start) | First start | Software lead + mentor |
| [3](#3-the-heads-limits-by-hand-posing) | The head's limits, by hand-posing | Mentor + two students |
| [4](#4-the-arms) | The arms: zeros, directions, test | Mechanical lead + mentor |
| [5](#5-start-by-itself) | Start by itself | Software lead |
| [6](#6-the-phone-face) | The phone face | Software lead |

> **One program on the motors at a time.** The robot software owns the motors while it runs.
> If a motor goes limp under it, it switches it back on and drives it home — even if someone is
> holding the head. Stop the software before running **any** motor script (Ctrl-C in its
> Terminal now; after step 5, `sudo systemctl stop reachy`).

---

## 1. Name and settings

Give the robot a **name** — the team's choice, short, easy to say, and **not like any other
robot's** (not "Ollie", and not two names that rhyme). The name is what the robot answers to,
and six robots with similar names means one call wakes six.

Open the settings file:

```bash
cd ~/reachy
nano .env
```

1. Find the line `WAKE_WORD=Ollie` (**Ctrl-W**, type `WAKE_WORD`, **Enter**) and change `Ollie`
   to your robot's name: `WAKE_WORD=Nova`.
2. Go to the very bottom of the file (**Ctrl-End**, or hold the down arrow) and add this line,
   which makes the voice come out of the phone in the head:
   ```
   SPEAK=face
   ```
3. **Ctrl-O**, **Enter** to save, **Ctrl-X** to exit. Leave everything else as it is.

## 2. First start

1. Check the calibration file one more time: `.venv/bin/python -m scripts.calibrate show` must
   say **`(loaded)`** and show your numbers.
2. Start the robot software by hand:
   ```bash
   ./run.sh
   ```
   The head rises to level and holds. **Keep a hand near the Power Hub's switch** the first
   time.
3. Open the web browser on the Pi and go to **`http://localhost:8080`** — the robot's
   **console**. It shows your robot and has buttons for its gestures, head poses and voice.
4. Go to **`http://localhost:8080/health`**. It should show `"backend": "dynamixel"`, and
   inside `"backend_health"`: `"motors"` listing 1–9, and `"calibrated": true`.
5. **Ctrl-C** in the Terminal stops the robot.

## 3. The head's limits, by hand-posing

*Mentor, with one student supporting the head and one at the keyboard.*

The robot knows where "level" is. Now it learns how far the head can go in each direction. The
capture tool needs the motors to itself, so the robot software must be stopped (Ctrl-C).

```bash
cd ~/reachy
.venv/bin/python -m scripts.calibrate show
.venv/bin/python -m scripts.calibrate capture pitch down 25
```

The head goes to level, then limp. Pose it to that limit, press **Enter**, and it saves the
motor positions and goes back to level. Do all eight:

| Command | Pose it to |
|---|---|
| `capture pitch down 25` / `capture pitch up -25` | chin down / chin up, as far as it goes comfortably |
| `capture roll right 20` / `capture roll left -20` | tilt to the robot's right / left |
| `capture yaw right 25` / `capture yaw left -25` | turn to the robot's right / left |
| `capture z up 12` / `capture z down -12` | lift the whole head straight up / lower it straight down |

⚠️ **Support the head at the chin *and* the crown, and rotate it — don't push it.** A hand on
the chin pushes the whole head down while it tips, and that slide gets recorded as part of the
nod: on Ollie the first nod came out as a forward head-thrust. The next command strips the slide
back out, using the two `z` captures as the reference. Keep the raw file first:

```bash
cp data/motor_calibration.json data/motor_calibration.raw.json
python3 scripts/clean_calibration.py
python3 scripts/clean_calibration.py --write data/cleaned.json
mv data/cleaned.json data/motor_calibration.json
.venv/bin/python -m scripts.calibrate show
```

The first `clean_calibration` line only reports; the second writes the cleaned file. `show`
must still say `(loaded)`. Copy **both** `motor_calibration.json` and
`motor_calibration.raw.json` onto the USB stick — the raw one is how the cleaning can be redone.

Now check the directions: start the robot (`./run.sh`) and on the console press **Look R**
(under *Head pose*). The head must turn to the robot's **own** right. Then drag the **Head roll**
slider (on the *Manual controls* card) to the right: the head must tilt to its own right. If one
is mirrored, the two captures for that axis were swapped — capture them again the other way
round.

## 4. The arms

The arms have no "level" to record. Each joint's **zero** is captured with the arm hanging
straight down, after it's built, and that's the reference every angle is measured from.

*The arm goes limp when you're not driving it, and a limp arm falls. Keep hands and faces clear
of it, and keep the mouse near the **PANIC** button. **Watch the first move of every joint** with
a hand ready on PANIC: these arms have never been zeroed on this robot before, and a joint that
has its sums wrong can try to go a long way.*

1. Start the robot (`./run.sh`) and open **`http://localhost:8080/limbs`** on the Pi.
2. Pick the **right** side. Press **🔍 Find motors** — it finds the arm's four motors and moves
   nothing. (The title at the top of the page always says "right arm"; trust the side buttons.)
3. Let the arm hang **at rest**: straight down, the forearm in line with the upper arm, the palm
   facing the body. Hold it still and press **⦿ Capture zero**.
4. Tick **Drive the real arm**. The arm switches on and holds exactly where it is.
5. **Check each joint's direction.** Move each slider a little way and watch the real arm:
   shoulder pitch should swing the arm forward, shoulder roll should lift it out to the side,
   the elbow should bend the forearm forward, and the wrist should turn the hand. If a joint goes
   the wrong way, press its **⇄** button — that's safe while the arm is live.

   **If a slider moves the wrong joint** — the pitch slider moves the roll joint, say — two motors
   are in each other's places, and ⇄ can't fix that. Untick **Drive the real arm**, pick the
   right motor from that joint's **id** list (picking one another joint holds swaps the two), press
   **🔍 Find motors**, and check the directions again.
6. Press **🎯 Test live robot**. It moves each joint a little, one at a time, and checks that it
   really moved. If it stops and lets the arm go limp, it found a joint that didn't move — a
   slipped belt or a stuck joint. Fix that before going on.
7. Untick **Drive the real arm**, pick the **left** side, and do steps 2–6 again.
8. **Make the arms come up with the robot:** stop the robot (Ctrl-C), open `.env` in `nano`,
   find `ARM_START=off` and change it to:
   ```
   ARM_START=both
   ```

An arm goes limp after about 15 seconds with no command and switches back on by itself at the
next one. That's normal, and it's what stops a motor holding a pose until it overheats.

## 5. Start by itself

When the head and both arms are calibrated, make the robot start whenever the Pi does:

```bash
cd ~/reachy
bash scripts/provision_pi.sh --service
sudo systemctl restart reachy
```

Restart the Pi (`sudo reboot`). About 15 seconds after the desktop appears, the head goes level
on its own and `http://localhost:8080` shows the console.

From now on **the robot software owns the motors whenever the Pi is on.** Before any motor
script:

```bash
sudo systemctl stop reachy
pgrep -af 'app\.main|app\.serve'
```

The second line must print **nothing** (if it prints anything, the software is still running).
Run your script, then `sudo systemctl start reachy` afterwards.

## 6. The phone face

The phone is set up **before** it goes into the head — once it's inside, its settings are hard to
reach.

1. **Check the battery:** the back glass must sit flat. A swollen phone never goes in a head.
2. Turn on **Stay awake**: *Settings → About phone → Software information*, tap **Build number**
   seven times to unlock Developer options, then *Settings → Developer options → Stay awake*.
3. Turn **auto-brightness off** and set the brightness by hand. Set the screen timeout to the
   maximum.
4. Put the phone on **the same wifi as the Pi**.
5. On the Pi, open **`http://localhost:8080/pair?audio=1`**. It shows a QR code. Scan it with the
   phone's camera, open the page, and in Chrome's menu (⋮) choose **Add to Home screen**. (The
   `?audio=1` matters: plain `/pair` makes the phone the eyes only, with no voice.)
6. Open the face from the new home-screen icon. **Tap it once** — phones stay silent until
   they're tapped. The eyes are **amber** until that tap, then they turn to normal.
7. Touch the face and press **🔊 Test audio**. It should speak.
8. **Into the head:** slide the phone into the face plate, **screen forward, charging port at the
   service-cap end**. The last few millimetres take a firm push — that's the plate's pads
   pressing the phone onto the front lip, and it's what stops the rattle. Plug in the charging
   cable, lead it out past the cap the way Ollie's is, and fit the service cap: tongue in,
   2 × M2 × 10 self-tapping. Don't pinch the cable.

Whenever the phone's page reloads — after the robot restarts, say — the eyes go amber again and
it needs one tap before it can make a sound.

**Back up:** copy `data/motor_calibration.json`, `data/motor_calibration.raw.json` and `.env`
onto the USB stick. (`.env` starts with a dot, so the file manager hides it — press **Ctrl-H** to
show hidden files.)

### ✅ Checkpoint 4

- [ ] `WAKE_WORD` in `.env` is set to the robot's own name
- [ ] After a restart it comes up by itself: the head goes level and holds, `/health` shows
      `"backend": "dynamixel"` and, inside `"backend_health"`, motors 1–9 and `"calibrated": true`
- [ ] **Look R** turns the head to the robot's own right, and **Head roll** tilts it the right way
- [ ] Both arms passed **🎯 Test live robot**, and `/health` shows both arms `"zeroed": true`
- [ ] The phone shows the eyes, speaks, and is charging inside the head
- [ ] The calibration files and `.env` are backed up on the USB stick
