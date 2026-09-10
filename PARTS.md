# Appendix A — Shopping list

Everything to **buy**. What to **print** is [Stage 1](1_PRINT.md). Quantities are **per robot**,
with a **×6** column for the whole program. Prices change; confirm each listing before ordering.

---

## Motors — the expensive part

| Part | Per robot | ×6 | Fleet spares | Notes |
|---|---:|---:|---:|---|
| **DYNAMIXEL XL330-M288-T** | 14 | 84 | 6 | 6 for the head, 4 for each arm. One of the original robot's motors arrived with a mis-moulded gear — buy spares |
| **DYNAMIXEL XL330-M077-T** | 2 | 12 | 1 | The antennae — a weaker, faster version. Don't mix them up with the M288 |
| **DYNAMIXEL XC330-M288-T** | 1 | 6 | 1 | The body turn. Metal case, because it turns the whole robot |

All three are 5 V motors on the same 3-pin cable. Each motor comes with one short cable.

## Motor bus and power

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| **ROBOTIS U2D2** | 1 | 6 | The USB adapter between the Pi and the motors |
| **ROBOTIS U2D2 Power Hub Board Set** | 1 | 6 | Where the motors plug in and get their 5 V |
| ROBOTIS Robot Cable-X3P, assorted lengths | 8 | 48 | Longer motor cables for the arms and the run up through the body — the stock ones are short |
| **12 V power brick**, 120 W or more | 1 | 6 | The robot's one plug for the motors and the phone. Ollie's is 160 W |
| **12 V → 5 V step-down converter, 10 A (50 W)** | 1 | 6 | Feeds the Power Hub, i.e. all 17 motors. ⚠️ The motors must only ever see **5 V** |
| 12 V → 5 V USB charger module (USB-A) | 1 | 6 | Charges the phone in the head |
| Fuse holder + 10 A fuses, rocker switch, wire, lever connectors, 2200 µF capacitor | 1 set | 6 | The mentor builds the power wiring from these — see [Appendix B](MENTOR_SETUP.md) |

## Brain — and the workbench

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| **Raspberry Pi 5, 4 GB** | 1 | 6 | Ollie runs on a 2 GB board and it is a real ceiling. 4 GB removes that |
| **Official Raspberry Pi 27 W USB-C power supply** | 1 | 6 | Not a generic 5 V supply — one measured 4.99 V on Ollie and made the Pi crash |
| microSD, 32 GB, high-endurance (Samsung PRO Endurance or SanDisk Max Endurance) | 1 | 6 | +2 spares. Label it with the robot number |
| Raspberry Pi 5 Active Cooler | 1 | 6 | |
| USB stick, 16 GB or more | 1 | 6 | The student kit, and the robot's calibration backups |
| **Monitor with HDMI**, USB keyboard and mouse | 1 set | 6 | The Pi is the workbench computer from Stage 2 on. Any school monitor and keyboard will do; they can be shared once a robot is finished |
| Micro-HDMI to HDMI cable | 1 | 6 | The Pi 5's video ports are micro-HDMI |

## Face

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| **Samsung Galaxy S10 (SM-G973)**, used is fine | 1 | 6 | The plain S10 — **not** the S10e, S10+ or S10 5G. The face plate is sized to this phone to a fraction of a millimetre. Check the screen has no burn-in and the battery isn't swollen. A different phone means a new face plate ([Stage 6](6_CUSTOMIZE.md)) |
| USB-A to USB-C cable, about 1 m, thin | 1 | 6 | From the USB charger in the base, up through the body, to the phone |

## Base and yaw joint

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| **6816-2RS thin-section bearing**, 80 × 100 × 10 mm | 1 | 6 | +1 spare |
| Brass spacer, ⌀6 mm OD × ⌀3.2 mm bore × 20 mm | 4 | 24 | R1 measures one of the body's four ⌀6.64 columns with a pin gauge **before** the fleet order |
| Stick-on rubber feet, ⌀12 mm | 8 | 48 | 4 for the plinth, 4 for the Pi case |

## Antenna wire

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| Stiff wire, brass or steel | about 50 cm | 3 m | Bent by hand into the two antennae. R1 measures the hole in the printed antenna hub and buys wire that's a snug push fit |

## Arms (both arms)

| Part | Per robot | ×6 | Notes |
|---|---:|---:|---|
| **GT2 closed-loop belt, 122 mm (61 teeth), 6 mm wide** | 4 | 24 | Shoulder pitch and shoulder roll, both arms. +1 spare per robot |
| **GT2 closed-loop belt, 140 mm (70 teeth), 6 mm wide** | 2 | 12 | The elbows. +1 spare per robot |

## Screws

The stock Reachy parts use the screws listed in the official
[Reachy Mini assembly guide](https://huggingface.co/spaces/pollen-robotics/Reachy_Mini_Assembly_Guide).
Buy each team an **M2 / M2.5 / M3 assortment** (machine screws, self-tapping screws and nuts)
for those. The custom parts need these specifically.

### Head, face and base

| Screw | Per robot | Where |
|---|---:|---|
| M2 × 5 self-tapping | 24 | Motor arms → motor boss (4 per arm) |
| M3 × 18 + M3 nut | 12 + 12 | Rods: through the ball into the motor arm, and the rod tops into the neck plate. R1 confirms the top-end length |
| M2 × 10–12 self-tapping | 2 | Face service cap |
| M2 × 8 | 4 | Yaw motor → the base's motor bridge |
| M2 × 10 | 4 | Yaw clamp → the yaw motor's boss |
| M3 × 8 countersunk | 3 | Yaw clamp → rotor, from below |
| M3 × 14 thread-forming | 6 | Base cap → plinth, sideways through the drum wall |
| Body clamshell screws, **longer than stock** | 4 | They now reach through the rotor into the body. R1 measures the length |
| M3 × 8–10 | 4 | U2D2 Power Hub Board → its tray |
| M2.5 × 8 | 8 | Pi → tray (4), cover → tray (4) |
| M3 × 16 thread-forming | 4 | Pi case → plinth wall |

### Arms — for both arms

| Screw | Per robot | Where |
|---|---:|---|
| M2 × 5 **countersunk** (90°, DIN 965) | 32 | Boss adapters (4 each × 6) and hand adapters (4 each × 2). Countersunk, not pan head: the seat is a cone |
| M2 × 8 | 6 | The centre screw in each small pulley |
| M2 × 16 | 18 | Big pulleys → their joints, 3 each |
| M2 × 16 **countersunk** | 4 | One per belt cover. Not shorter — the screw crosses the cover's own boss first |
| M2 × 6 | 8 | Pitch and elbow motors, 2 each |
| M2 washer, about 5 mm across | 4 | Under the elbow motors' screws |
| M2 × 20 self-tapping | 4 | Roll motors, 2 each |
| M3 × 12 | 4 | Wrist clamps, 2 each |
| M3 × 10 self-tapping, or a 2.5 mm pin | 2 | Pins each pitch shaft to its fork |
| M3 × 12 + M3 nut | 8 + 8 | Shoulder housings → body shell, 4 each. R1 confirms the length |

## Tools

**Per team:** metric hex keys and small screwdrivers (Phillips #0 and #1, and a small flat blade
for belt tension), digital calipers, a multimeter, a drill with 2.5 mm and 3.2 mm bits, a small
vice (for pressing bushings), a small spirit level (or a phone level app), flush cutters,
needle-nose pliers, a file, zip ties, painter's tape and a marker, a hot-glue gun, a deburring
tool and fine sandpaper.

**Shared:** a kettle and a thermometer (ball joints are swaged in 80–90 °C water), a pin gauge
set or drill bits to measure holes, and a Meta Quest headset for the VR test in Stage 5.
