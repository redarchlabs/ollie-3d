# Stage 1 — Print everything

**Everything gets printed before anything gets built.** Printing takes days and the build takes
hours, and a part that doesn't fit is far cheaper to find now than halfway through the
assembly. The print lead owns this stage; everyone else can help sort, clean up and label parts
as they come off the printer.

Use the files in the **`print/`** folder — in the **ollie-3d** repository, or on your team's
USB stick. They are already in millimetres and already turned the right way up, so **print
everything at 100 %, and don't rotate the arm parts**. (If you take a file straight from the
robot's main repository instead: the stock Reachy parts in `hardware/oem/` are modelled in
metres and import 1000× too small.)

**Default settings** unless a row says otherwise: **PETG, 0.2 mm layers, 3 walls, 15–20 %
infill.**

---

## 1. Test prints — before anything else

Each of these is small and answers one question that would otherwise cost a big print. R1
prints them first; the other teams print them once R1's have passed. Write every result in the
team log.

| Print | File | Question it answers | Pass when |
|---|---|---|---|
| Hug test | `eye_hug_test.stl` | How much grip does *your* printer and plastic give a ball joint? | A ball pressed into the longest-stub eye can't be pulled off by hand |
| Balls | `balls_production_9.05_x6.stl` | Are the balls the right size? | Calipers read **9.00–9.10 mm**. At 8.95 the joint holds half as well |
| One rod | `rod_v6_eye_rod_122mm.stl` | Does the snap ring hold a ball? | Ball swaged in warm (Stage 3), swivels freely, won't pull out |
| One motor arm | `arm_30mm.stl` | Does the arm fit the motor and the rod? | Sits flat on the motor's round boss, 4 × M2 screws bite, the rod bolts on |
| Yaw clamp | `yaw_clamp.stl` | Does the base's hardest joint fit the body-turn motor? | Its nose seats on the XC330's boss with no rocking. **Print it nose up** |
| Face plate | `s10_face_plate.stl` + `s10_face_cap.stl` | Does *your* S10 fit? | Test it the way it goes in the head — **charging port at the service-cap end, cable plugged in**. The phone slides in with a firm push at the end, the cap screws shut over the cable, nothing rattles or rocks |
| **Arm joint coupon** | `coupon_joints.stl` | Do the arm's two printed-in-place joints come out loose enough to turn? | After breaking them loose by hand, both joints turn with a fingertip. **This is the most important test print** — the first arm came off the bed with its elbow welded solid |
| **Hand snap** | `hand_adapter.stl` + `hand.stl` | Does the hand's snap fit your printer? | The hand pushes onto the adapter and clicks; it pulls off only with effort. An over-squashed first layer makes the snap too tight, and a snap that won't flex splits the hand |

If a test fails, **stop and tell the mentor** before printing the real parts. A fit is the one
thing only your printer can answer.

---

## 2. Print list — one robot

`print/PRINT_LIST.csv` is the same list, with a *done* column to tick off.

### Head and neck

| Part | File | Qty | Notes |
|---|---|---:|---|
| Head back | `head_back.stl` | 1 | Supports under the openings |
| Crown cover | `head_mic.stl` | 1 | **Easy to forget** — without it the top of the head is an open slot |
| Face plate | `s10_face_plate.stl` | 1 | Face **down** on the bed, no supports. Sized for a Galaxy S10 only |
| Service cap | `s10_face_cap.stl` | 1 | Tongue side down, no supports |
| Neck plate | `neck_reference.stl` | 1 | 20 % infill. Its six numbered holes take the rod tops |
| Stewart main plate | `stewart_main_plate.stl` | 1 | 20 % infill |
| Stewart tricap | `stewart_tricap.stl` | 1 | 20 % infill |
| **Rods** | `rod_v6_eye_rod_122mm.stl` | 6 (+2 spare) | **0.15 mm layers**, no supports, lying flat, 4 walls, 40 %+ infill. It must be the `v6_eye` file — see below |
| **Balls** | `balls_production_9.05_x6.stl` | 2 plates (12 balls) | As oriented (bore down), 0.10–0.15 mm layers. Print a third plate for spares |
| **Motor arms** | `arm_30mm.stl` | 6 (+2 spare) | Flat, **4 walls, 50 %+ infill** — these carry full motor torque |

> ⚠️ **The rod file is `rod_v6_eye_rod_122mm.stl` and nothing else.** The robot's main
> repository also holds older lengths and other joint styles, and one of them has been printed
> by mistake before. The right one has a raised collar around the ball hole on **both** faces.

### Antennae

| Part | File | Qty | Notes |
|---|---|---:|---|
| Antenna hub | `antenna_body.stl` | 2 | One per antenna |
| Antenna interface | `antenna_interface.stl` | 2 | One per antenna |
| Motor holder, left | `antenna_holder_l.stl` | 1 | 20 % infill |
| Motor holder, right | `antenna_holder_r.stl` | 1 | 20 % infill |

The antennae themselves aren't printed: they're stiff wire, bent by hand in Stage 3.

### Body

| Part | File | Qty | Notes |
|---|---|---:|---|
| Body top | `body_top.stl` | 1 | Supports under the openings. Long print — start early. The arms screw to it |
| Body bottom | `body_down.stl` | 1 | Supports under the openings |

### Base, yaw joint and Pi case

| Part | File | Qty | Notes |
|---|---|---:|---|
| Plinth | `base_body.stl` | 1 | **About ten hours.** Upright, no supports, 20 % infill. Turn on bridge detection (the window ceiling is a 62 mm bridge) |
| Stator (cap) | `base_top.stl` | 1 | Flat, upright, no supports, **25–30 % infill** — carries the robot |
| Rotor | `yaw_rotor.stl` | 1 | Flat, upright, no supports, **25–30 % infill** |
| Clamp / drive hub | `yaw_clamp.stl` | 1 | **Print it NOSE UP** — flat on the bed puts the nose under the bed. Keep your test print if it passed |
| U2D2 tray | `u2d2_tray.stl` | 1 | No supports |
| Shelf (optional) | `base_shelf.stl` | 1 | Disc down, legs up, no supports |
| Pi case tray | `pi5_tray.stl` | 1 | As it loads, no supports, 20 % |
| Pi case cover | `pi5_cover.stl` | 1 | **Upside down** — roof flat on the bed |

### Arms — both arms

Every arm file in the kit is **already the right way up**. The two `arm_printed` parts are the
exception to every other habit you have: **don't rotate them on the bed**, because their
joints are printed in place and the gaps in them are sized for exactly that orientation.

| Part | File | Qty | Notes |
|---|---|---:|---|
| **Arm, left** | `arm_printed_left.stl` | 1 | The shoulder fork, upper arm and forearm in **one print, with both joints printed in place**. As loaded, don't rotate. Support **on build plate only** |
| **Arm, right** | `arm_printed_right.stl` | 1 | The mirror image — not the same part. Same rules |
| Shoulder housing | `shoulder_housing.stl` | 2 | As loaded, don't rotate. It screws to the body |
| Hand | `hand.stl` | 2 | Serves both arms |
| Hand adapter | `hand_adapter.stl` | 2 | The hand snaps onto it |
| Wrist clamp | `wrist_clamp.stl` | 2 | Holds the wrist motor in its cradle |
| Boss adapter | `boss_adapter.stl` | 6 | Printed on its side, as loaded |
| Small pulley, 20 teeth | `pulley_20t.stl` | 6 | On each belted motor |
| Big pulley, 40 teeth | `pulley_40t_flange.stl` | 6 | On each joint |
| Roll belt cover, left | `belt_cover_roll_left.stl` | 1 | Flat, no supports |
| Roll belt cover, right | `belt_cover_roll_right.stl` | 1 | Flat, no supports. The mirror of the left |
| Elbow belt cover | `belt_cover_elbow.stl` | 2 | Flat, no supports. Serves both arms |
| Bushing | `bushing.stl` | 4 | Two per shoulder housing |
| Pitch shaft | `shaft_pitch_44mm.stl` | 2 | **Lying down** — stood up, it snaps along its layers |
| Shaft collars | `collar_2mm.stl`, `collar_3mm.stl`, `collar_4mm.stl` | 2 each | Shims for the pitch shaft. Print all three sizes; Stage 3 uses whichever fits |

Three rules for the two `arm_printed` parts, all learned from arms that came off the bed stuck:

- **Support on build plate only.** A slicer allowed to support *everywhere* will try to fill the
  0.4–0.7 mm gaps inside the joints, and a joint with support inside it never moves.
- **If the slicer offers to "repair", "merge" or "make solid", say no.** Each file is six separate
  pieces on purpose — the gaps between them *are* the joints.
- **Don't over-squash the first layer.** It eats the joint's clearance on its own.

**Weigh the first `arm_printed`** as it comes off: about 62 g. If it's far off that, tell the
mentor — the arm's strength numbers assume it.

### Do **not** print

- `head_front.stl` — replaced by the S10 face plate.
- `body_foot.stl` and `body_turning.stl` — replaced by the printed base and yaw joint.
- `pitch_fork.stl`, `upper_arm.stl`, `forearm.stl` — these are the arm's parts drawn separately
  for the 3D preview. They can never be joined; `arm_printed` is the file.
- `shoulder_spine.stl` — it ties the two shoulders together for an arm built on its own. On this
  robot the shoulders screw straight to the body shell instead.
- Anything in the main repository's `hardware/oem/reference/` — those are models of parts you
  **buy**.

None of these are in `print/`, which is the easiest way to avoid printing them.

### How much plastic

One robot is about **1.5 litres of solid plastic** — 1.2 litres for the head, body and base and
0.35 for the two arms (measured off the files). At the infills above that prints at roughly
**1.3 kg of PETG per robot**. Test pieces, spares and reprints add about half as much again, so
**order about 12 kg of PETG for six robots**.

---

## 3. Label everything

As each part comes off the printer: clean off supports and brims, then write the robot number
on a hidden face in pencil or marker, and put it in the robot's bin. Left and right parts go in
separate bags marked **L** and **R** — the left and right arm parts look alike and are not the
same.

### ✅ Checkpoint 1

- [ ] Every test print passed, and the results are in the team log
- [ ] Every part on the print list is printed and ticked off in `PRINT_LIST.csv`
- [ ] Both `arm_printed` parts weighed, and their joints not yet forced (Stage 3 breaks them loose)
- [ ] Every part labelled with the robot number; left and right arm parts bagged separately
