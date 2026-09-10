# Stage 6 — Make it yours (optional)

Your robot works. Everything in this chapter is optional, and none of it should be started until
your robot has passed Stage 5 — a customisation is much easier to trust on a robot you already
know works.

| Customisation | Effort | Who |
|---|---|---|
| [Name, voice and eyes](#name-voice-and-eyes) | Minutes, on the console | Anyone |
| [Your own head, designed in Blender](BLENDER.md) | Days — design, check, print | Designer + team |
| [A different phone for the face](#a-different-phone) | A reprinted face plate | Mentor + team |

---

## Name, voice and eyes

- **Name.** `WAKE_WORD` in `.env` (Stage 4). Change it with `nano .env`, then
  `sudo systemctl restart reachy`.
- **Voice.** The console's **🗣️ Speech & voice** card picks the robot's voice from a list of
  characters, and has sliders for how fast it talks. The robot remembers your choice after a
  restart.
- **Eyes.** Touch the phone's face and a bar rises from the bottom: **◀ / ▶** step through 36
  eye styles, named as you go. Pick one before the head is closed up.
- **A more natural voice (mentor).** Out of the box the Pi speaks with *espeak*, which sounds
  properly robotic. For smoother voices, on the Pi:
  ```bash
  cd ~/reachy
  bash scripts/fetch_voices.sh
  bash scripts/provision_pi.sh --voices
  sudo systemctl restart reachy
  ```
  It needs internet and about 500 MB of space.

## Your own head

The next chapter, [Designing your robot's head in Blender](BLENDER.md), is the big one. You
start from the standard head and add ears, horns, a crest, a visor or your robot's name, and a
script checks your design against every rule the robot needs before it exports the file you
print. Blender runs on a Windows, Mac or Linux computer — use a school computer for it, not the
robot's Pi.

---

## A different phone

The face plate is made for a **Samsung Galaxy S10** (model SM-G973) to a fraction of a
millimetre: 149.9 × 70.4 × 7.8 mm, 157 g. The plain S10 — not the S10e, S10+ or S10 5G. A
different phone means a **new face plate**, made by the mentor from the phone's measurements.

**A phone is a good candidate if:**

- it's **Android with Chrome**. An iPhone can show the face, but it can't reopen the page by
  itself after a power cut, and a sealed head needs that;
- it's **close to the S10's size**. The S10 is already as wide as the head (150 mm), so a longer
  phone sticks out at the sides;
- it's **no heavier than 157 g**. Six small motors hold the head up, and the phone is most of its
  weight;
- it has an **OLED screen** if possible, so the black around the eyes is truly black;
- its battery is **not swollen** — the back sits flat.

**Making the new plate:**

1. **Measure the phone** with calipers, to 0.1 mm: length, height, thickness. Weigh it. Note
   where its rear camera bump is.
2. **Mentor:** put the three measurements into `PHONE_W`, `PHONE_H` and `PHONE_T` at the top of
   `hardware/s10-face/generate_s10_face.py` in the robot's main repository, regenerate the plate
   and cap, and run the fit check (`verify_s10_face.py`). The S10's camera relief (`CAM`) and screen window (`WIN_W`, `WIN_H`)
   are there too. The file's README says how.
3. **Print a test plate first**, exactly like the face-plate test print in Stage 1: the phone
   slides in with a firm push at the end, the cap screws shut, and nothing rattles.
4. **Set the eyes' size** on the new phone: touch the face, press **⚙**, hold a ruler against the
   blue bar and adjust it until it is **exactly 50 mm**. The face then draws its eyes at the right
   size on that screen.
5. Set the new phone up as in Stage 4, step 6 — Stay awake, brightness, pairing, one tap.

⚠️ A heavier phone changes how the head moves. After fitting one, re-run the acceptance test in
Stage 5, and if the head sags or struggles to reach its limits, go back to the S10.
