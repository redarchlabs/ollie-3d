# Appendix B — Mentor notes

This appendix is for the adults. It covers what has to be ready before the students start, and
the parts of the build that can break hardware if they're done in the wrong order.

---

## Before day one

### 1. The student kit — one USB stick per team

On a computer with the robot's main repository (`redarchlabs/reachy-the-robot`):

```bash
.venv-cad/bin/python docs/student-build/make_pdf.py
.venv-cad/bin/python scripts/make_student_kit.py
```

That writes `dist/reachy-student-kit/` (and a zip of it). Copy the folder onto six USB sticks
labelled R1–R6. The kit holds the print files (all millimetres), this book, the Blender starter,
and `software/reachy-software.tar.gz`: the robot software as committed, plus the 3D models and
browser libraries (Blockly, three.js) its pages need. It deliberately holds **no** `.env`, no
calibration and no voice models — a student robot starts clean.

The same print files, this book's chapters and the Blender starter are published to the
**ollie-3d** repository, without the software:
`.venv-cad/bin/python scripts/export_ollie3d.py <your ollie-3d checkout>`, then commit and push
there.

### 2. The SD cards

Raspberry Pi Imager → **Raspberry Pi 5** → **Raspberry Pi OS (64-bit)**, the version with the
desktop. In the Imager's settings:

- hostname `reachy-r1` … `reachy-r6`;
- a username and password — write them down; the install in Stage 2 asks for the password;
- the wifi the robots will use, and your country, time zone and keyboard;
- SSH, if you want to reach the Pis from a laptop (optional — nothing in the book needs it).

Label each card with its robot number.

### 3. The network

Two things are needed from the wifi, and school networks often give only the first:

1. **Internet**, for the install in Stage 2 (system packages and Python packages).
2. **Devices that can reach each other.** The phone in the head, the Pi and (for the VR test)
   the headset all talk to each other directly. Many school networks block that ("client
   isolation"), and it shows up as a phone that simply can't open the robot's page. If so, bring
   a travel router and put the robots on its wifi.

Reserve each Pi's address in the router (a DHCP reservation) so it never changes — the phone's
home-screen icon has the address in it.

### 4. Don't deploy student robots from Ollie's working copy

`scripts/deploy_pi.sh` was written for Ollie. On any Pi that doesn't have them yet, it seeds two
files from the working copy it runs in: Ollie's **`.env`** (with its credentials) and Ollie's
**`data/motor_calibration.json`** — motor positions measured on a different head, which can drive
a student head against its own rods and break a printed rod or motor arm. Student robots are
installed from the kit, on the Pi, as Stage 2 describes. If you ever do use `deploy_pi.sh` for a
student Pi, run it from a fresh clone, which has neither file.

---

## The power wiring (12 V)

```
 wall ─ 12 V brick ─[10 A fuse]─[switch]─┬─► 12→5 V converter, 10 A ──► U2D2 Power Hub ──► 17 motors
                                         └─► 12→5 V USB charger ──────► phone, up the neck

 wall ─ official Pi 27 W supply ──► Raspberry Pi 5   (its own supply — never the 12 V board)
```

Build it from **`hardware/power/BUILD.md`** in the main repository, which puts a meter reading between
every step. The student robots use two of its outputs: the motor converter and the phone's USB
charger. The Pi stays on its official supply — a general-purpose 5 V supply measured 4.99 V on
Ollie, close enough to the Pi's cut-out that it crashed.

- Fuse the **+12 V** leg, not ground. Nothing above 12 V goes inside the base.
- **Set and measure the motor converter at 5.0 V with nothing connected**, then at the Power
  Hub's input, and only then connect motors. A 12 V mistake here destroys every motor on the bus.
- **Seventeen motors on one 10 A converter** is what Ollie runs. A driven arm holds itself up
  against gravity, so the converter works hardest while the arms are moving. Feel it after the
  30-minute run in Stage 5, which includes arm shows: warm is fine; too hot to hold means the
  arms need a converter of their own.
- Tie every wire down. Ollie's motors once lost power for eleven minutes and came back only when
  the cables in the base were moved — most likely a short from a loose wire.

---

## The calibration file

Students write it in Stage 3 from `calibration-template.json`, which is in the software:

```json
{
  "joints": {
    "antenna_left":  {"id": 1, "center": 2048, "ticks_per_deg": 11.4,
                      "sign": 1, "min": 1024, "max": 3072},
    "antenna_right": {"id": 2, "center": 2048, "ticks_per_deg": 11.4,
                      "sign": -1, "min": 1024, "max": 3072},
    "body_yaw":      {"id": 3, "center": 2048, "ticks_per_deg": 11.4,
                      "sign": 1, "min": 512, "max": 3584}
  },
  "head": {
    "ids": [4, 5, 6, 7, 8, 9],
    "neutral": [2048, 2048, 2048, 2048, 2048, 2048],
    "presets": {},
    "jacobian": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                 [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
  }
}
```

- `neutral` is the six "level" readings, in ID order 4–9. Each must be between about 1000 and
  3100, or that arm's travel crosses the motor's 4095 → 0 seam.
- Each `center` is read with the part in its middle position; `min`/`max` stay the same distance
  from it as above (antennae ±1024, body ±1536) and inside 0–4095.
- The **all-zero `jacobian` is deliberate**: until the head's limits are captured in Stage 4,
  every head command holds level instead of guessing.
- The head's limits (Stage 4) and the arms' zeros (captured on `/limbs`) are written into the
  same file by the software. None of it can be regenerated — it was measured on that robot —
  which is why the book keeps asking for backups.

**Two traps in the tools, and why the book says "`show` first" so often:**

- Every `calibrate` command **except `show`** opens the motor port and drives the head to
  "home" before doing anything else.
- `calibrate` quietly falls back to built-in defaults when the file is missing or has a typo,
  and the default "home" is 2048 on every head motor — up to about 50° from level on a head with
  its rods fitted. So `show` must say `(loaded)` before anything else runs.

The robot software does the same when it starts: it switches the motors on and drives the head to
level straight away. That's why the autostart isn't installed until Stage 4, step 5, when the
calibration is complete.

---

## The phone

- Plain http is enough for the **eyes and the voice** — no certificate.
- Phones stay silent until tapped, and that permission is lost every time the page reloads, so
  the eyes go amber after a restart until someone taps the face. *Fully Kiosk Browser* (Android)
  can remove the tap and reopen the page when the phone restarts; see
  `hardware/phone-eyes/README.md`.
- The phone's **microphone and camera** need https that the phone trusts (an mkcert certificate
  authority installed on the phone). That isn't part of this build; the top-level `README.md`
  of the main repository covers it.

## The certificate for VR

`scripts/make_cert.sh` (Stage 5) uses `mkcert` if it's installed, and otherwise makes a
self-signed certificate — that's the "Advanced → Proceed" warning. Once a certificate exists the
robot serves **https on 8080 and plain http on 8081**, which is why the phone face has to be
re-added on 8081. To undo it: `rm -r ~/reachy/certs` and `sudo systemctl restart reachy`, and the
phone's old icon on 8080 works again.

### VR head directions

VR steers the real head from the wearer's head, and the three directions are set by
`YAW_SIGN`, `PITCH_SIGN` and `ROLL_SIGN` near the top of `app/static/vr.js`, which the file marks
as not yet checked on hardware. If Stage 5 finds an axis backwards, flip that one constant in the
main repository and rebuild the kit. It's the same code on every robot, so R1's result is
everyone's.

## Updating a robot's software later

Build a new kit, copy the new `reachy-software.tar.gz` into the Pi's home folder, and:

```bash
tar -xzf reachy-software.tar.gz
cd ~/reachy
bash scripts/provision_pi.sh
sudo systemctl restart reachy
```

The archive has no `data/` files and no `.env`, so unpacking it over the old copy leaves the
robot's name, settings and calibration alone.

## What still needs tooling (for whoever picks this up)

- There is no `calibrate capture-neutral`: Stage 3 reads positions with `motor_status.py` and
  the file is edited by hand in `nano`. A command that reads with the head limp — and never
  homes first — would remove the hand edit.
- `calibrate` falls back to defaults on a missing or broken file and then homes to them.
  Refusing to move when the file can't be read would make the `show` ritual unnecessary.
- The arms' mount to the body is a hand-fitted, drilled joint. A printed bracket or a drilling
  template would make six robots match without R1's measurements.
