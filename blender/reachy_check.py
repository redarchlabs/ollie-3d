# reachy_check.py — check your Reachy head design, then export it for printing.
#
# HOW TO USE
#   1. Put things you want to ADD to the head (ears, horns, fins, raised letters) in the
#      "MY ADD-ONS" collection, and things you want to CARVE OUT of it (engraved letters,
#      grooves) in "MY CUTS". Each one must be a closed solid.
#   2. Save the .blend file (File > Save).
#   3. In this Text Editor, press  Run Script  (the ▶ button, or Alt+P).
#   4. Read the report that opens here. PASS means your STL files are in the "export"
#      folder next to your .blend. FAIL means nothing was exported — fix the lines marked FIX.
#
# The rules are the same ones the original character heads were designed to
# (hardware/heads/CHARACTER_SPEC.md, section 0). Mentors: they live in the constants below.

import math
import os
import re

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

# ── Your settings ─────────────────────────────────────────────────────────────────────
ROBOT = "R1"            # your robot's number, R1..R6
DESIGN = "my-head"      # a short name for your design: letters, numbers and dashes
KEEP_ANTENNAE = True    # False ONLY if your robot will have no antennae

# ── The rules ─────────────────────────────────────────────────────────────────────────
PETG_G_PER_CM3 = 1.27   # solid PETG. Thin shells print nearly solid, so this is honest
SHELL_MAX_G = 65.0      # the whole back shell, base part + your add-ons
FACE_ADD_MAX_G = 15.0   # what you add to the face plate
SEAM_Y = -30.75         # where the face plate meets the back shell (the face is at -Y)
FACE_PLANE_Y = -43.0    # the flat front of the face plate
FACE_FRONT_Y = -48.0    # face details may stand at most 5 mm proud of it
MAX_ABS_X = 88.0        # widest the head may get, each side
MAX_Z = 75.0            # tallest (horns, crests)
MAX_Y = 52.0            # furthest back
SHELL_MIN_Z = -39.0     # the shell's open bottom; the neck is below it
FACE_MIN_Z = -47.0      # the face plate's chin
MOTION_MARGIN = 2.0     # mm of daylight to the body at every head pose
PIVOT = Vector((0.0, 0.0, -40.0))  # the head turns about the neck base (robot3d.js)

# How far the head really moves: the calibration's captured stops (docs/student-build/
# MENTOR_SETUP.md, step C), which the head never goes past — pitch +-25 (+ = nod down),
# roll +-20, yaw +-25, lift +-12 mm. Every add-on is swept through these against the body.
PITCHES = (-25.0, -12.5, 0.0, 12.5, 25.0)
ROLLS = (-20.0, 0.0, 20.0)
YAWS = (-25.0, 0.0, 25.0)
LIFTS = (-12.0, 0.0, 12.0)
MAX_SWEEP_POINTS = 3000

# Collection and object names the starter file uses. Don't rename them.
ADD_COLLECTION = "MY ADD-ONS"
CUT_COLLECTION = "MY CUTS"
RESULT_COLLECTION = "RESULT (what gets printed)"
BASE_SHELL = "BASE_shell"
BASE_FACE = "BASE_face"
BODY = "REF_body_top"
REPORT_TEXT = "CHECK REPORT"

# Which keep-out zones apply to what. part: "shell", "face" or "any".
KEEP_OUTS = {
    "KO_inside_head": dict(part="shell", addons=True, cuts=True,
                           why="it reaches inside the head, where the head's own parts are"),
    "KO_plate_band": dict(part="shell", addons=True, cuts=True,
                          why="it reaches in where the face plate slots into the shell"),
    "KO_phone_pocket": dict(part="face", addons=True, cuts=True,
                            why="it reaches into the phone pocket behind the face"),
    "KO_eyes": dict(part="face", addons=True, cuts=False,
                    why="it covers an eye — the phone draws the eyes there"),
    "KO_glass": dict(part="face", addons=True, cuts=False,
                     why="it would press on the phone's glass"),
    "KO_service": dict(part="any", addons=True, cuts=True,
                       why="it blocks the service cap — the phone slides out that side to charge"),
    "KO_neck": dict(part="any", addons=True, cuts=False,
                    why="it hangs below the head, where the neck and body are"),
    "KO_antennae": dict(part="any", addons=True, cuts=False, antenna=True,
                        why="the antennae swing through there and would hit it"),
}


# ── Geometry helpers ──────────────────────────────────────────────────────────────────

def world_bmesh(obj: bpy.types.Object, weld: bool = False) -> bmesh.types.BMesh:
    """The object's evaluated mesh (modifiers applied) in world coordinates.

    weld: merge coincident vertices. A Text object's mesh has its faces and sides as
    separate pieces that only touch, so it reads as full of holes until they are joined."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    evaluated.to_mesh_clear()
    bm.transform(obj.matrix_world)
    if weld:
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-4)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm


def is_closed(bm: bmesh.types.BMesh) -> bool:
    return len(bm.faces) > 0 and all(e.is_manifold for e in bm.edges)


def volume_cm3(bm: bmesh.types.BMesh) -> float:
    return abs(bm.calc_volume(signed=True)) / 1000.0


def sample_points(bm: bmesh.types.BMesh, limit: int) -> list:
    points = [v.co.copy() for v in bm.verts] + [f.calc_center_median() for f in bm.faces]
    step = max(1, len(points) // limit)
    return points[::step]


_RAY = Vector((0.5773503, 0.5773504, 0.5773501)).normalized()  # skewed: never along an edge


def inside(bvh: BVHTree, point: Vector) -> bool:
    """Inside a closed mesh: a ray from the point crosses its surface an odd number of times.

    Not "the nearest face points away from me" — that reads a point beside a sharp edge as
    inside, and on the first run it put probes 0.8 mm OUTSIDE every keep-out inside one.
    Parity needs each tested mesh to be one closed piece, which is why keep-outs made of
    overlapping pieces are tested one island at a time."""
    crossings = 0
    origin = point.copy()
    for _ in range(64):
        location, _, _, _ = bvh.ray_cast(origin, _RAY)
        if location is None:
            break
        crossings += 1
        origin = location + _RAY * 1e-4
    return crossings % 2 == 1


def island_trees(bm: bmesh.types.BMesh) -> list:
    """One BVH per connected piece of the mesh."""
    parent = list(range(len(bm.verts)))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    bm.verts.index_update()
    for f in bm.faces:
        first = root(f.verts[0].index)
        for v in f.verts[1:]:
            parent[root(v.index)] = first
    groups: dict = {}
    for f in bm.faces:
        groups.setdefault(root(f.verts[0].index), []).append(f)
    trees = []
    for faces in groups.values():
        index = {}
        verts, polys = [], []
        for f in faces:
            poly = []
            for v in f.verts:
                if v.index not in index:
                    index[v.index] = len(verts)
                    verts.append(v.co.copy())
                poly.append(index[v.index])
            polys.append(poly)
        trees.append(BVHTree.FromPolygons(verts, polys))
    return trees


def touches(bvh_a: BVHTree, islands_b: list, points_a: list) -> bool:
    return any(bool(bvh_a.overlap(t)) or any(inside(t, p) for p in points_a) for t in islands_b)


def pose_matrix(pitch: float, roll: float, yaw: float, lift: float) -> Matrix:
    rotation = (Matrix.Rotation(math.radians(pitch), 4, "X")
                @ Matrix.Rotation(math.radians(roll), 4, "Y")
                @ Matrix.Rotation(math.radians(yaw), 4, "Z"))
    return (Matrix.Translation(PIVOT + Vector((0.0, 0.0, lift)))
            @ rotation @ Matrix.Translation(-PIVOT))


def bounds(bm: bmesh.types.BMesh) -> tuple:
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))


# ── The checks ────────────────────────────────────────────────────────────────────────

class Report:
    def __init__(self) -> None:
        self.lines: list = []
        self.failed = False

    def ok(self, text: str) -> None:
        self.lines.append(f"  OK    {text}")

    def fix(self, text: str) -> None:
        self.lines.append(f"  FIX   {text}")
        self.failed = True

    def note(self, text: str) -> None:
        self.lines.append(f"  NOTE  {text}")

    def head(self, text: str) -> None:
        self.lines.append("")
        self.lines.append(text)


def collection_objects(name: str) -> list:
    coll = bpy.data.collections.get(name)
    if coll is None:
        return []
    return [o for o in coll.all_objects if o.type in {"MESH", "CURVE", "FONT", "META", "SURFACE"}]


def keep_out_trees() -> dict:
    trees = {}
    for name in KEEP_OUTS:
        obj = bpy.data.objects.get(name)
        if obj is not None:
            bm = world_bmesh(obj)
            trees[name] = island_trees(bm)
            bm.free()
    return trees


def which_part(name: str, y_range: tuple, report: Report) -> str | None:
    y_min, y_max = y_range
    if y_max <= SEAM_Y:
        return "face"
    if y_min >= SEAM_Y:
        return "shell"
    report.fix(f"{name}: crosses the line where the face plate meets the back shell "
               f"(Y = {SEAM_Y}). Split it into two objects, one each side.")
    return None


def check_item(obj, kind: str, trees: dict, bases: dict, report: Report) -> dict | None:
    """Check one add-on or cut. Returns its facts, or None if it can't be used."""
    if kind == "cuts":
        obj.display_type = "WIRE"   # so the cut doesn't hide what it cuts
    bm = world_bmesh(obj, weld=True)
    try:
        if not bm.verts:
            report.fix(f"{obj.name}: has no geometry")
            return None
        if not is_closed(bm):
            report.fix(f"{obj.name}: isn't a closed solid (it has holes or loose edges). "
                       "Try Mesh > Clean Up > Fill Holes, or 3D Print Toolbox > Make Manifold.")
            return None
        (x0, x1), (y0, y1), (z0, z1) = bounds(bm)
        part = which_part(obj.name, (y0, y1), report)
        if part is None:
            return None
        points = sample_points(bm, MAX_SWEEP_POINTS)
        tree = BVHTree.FromBMesh(bm)
        problems = []

        for ko_name, rule in KEEP_OUTS.items():
            if ko_name not in trees or not rule[kind]:
                continue
            if rule.get("antenna") and not KEEP_ANTENNAE:
                continue
            if rule["part"] not in ("any", part):
                continue
            if touches(tree, trees[ko_name], points):
                problems.append(f"{obj.name}: {rule['why']} ({ko_name})")

        if kind == "addons":
            if max(abs(x0), abs(x1)) > MAX_ABS_X:
                problems.append(f"{obj.name}: sticks out {max(abs(x0), abs(x1)):.1f} mm to the "
                                f"side — the limit is {MAX_ABS_X:.0f}")
            if z1 > MAX_Z:
                problems.append(f"{obj.name}: reaches Z {z1:.1f} — the limit is {MAX_Z:.0f}")
            if y1 > MAX_Y:
                problems.append(f"{obj.name}: reaches {y1:.1f} mm back — the limit is {MAX_Y:.0f}")
            floor = SHELL_MIN_Z if part == "shell" else FACE_MIN_Z
            if z0 < floor:
                problems.append(f"{obj.name}: hangs down to Z {z0:.1f} — nothing may go below "
                                f"{floor:.0f} on the {part}")
            if part == "face" and y0 < FACE_FRONT_Y:
                problems.append(f"{obj.name}: stands {FACE_PLANE_Y - y0:.1f} mm proud of the face "
                                f"— the limit is {FACE_PLANE_Y - FACE_FRONT_Y:.0f} mm")
            base_tree, _ = bases[part]
            if not bool(tree.overlap(base_tree)):
                problems.append(f"{obj.name}: doesn't touch the {part}. Sink it about 1 mm into "
                                "the surface, or it prints as a separate loose piece")
        else:
            base_tree, _ = bases[part]
            if not bool(tree.overlap(base_tree)):
                problems.append(f"{obj.name}: doesn't reach the {part}, so it would cut nothing")

        for p in problems:
            report.fix(p)
        if not problems:
            report.ok(f"{obj.name} ({part}): closed, attached, clear of every keep-out zone")
        return dict(obj=obj, part=part, points=points, volume=volume_cm3(bm),
                    usable=not problems)
    finally:
        bm.free()


def sweep_motion(items: list, base_points: list, body_tree: BVHTree, report: Report) -> None:
    """Move every add-on through the head's range and measure how close it comes to the body.

    Judged against the standard head at the SAME pose, not against a fixed number: at the
    bottom of a nod Ollie's own chin reaches the body (that is where the nod stops), so a
    fixed margin would fail every face add-on, including ones that change nothing there.
    An add-on fails if it comes within MOTION_MARGIN of the body AND closer than the
    standard head already does.

    Plain distance, not inside/outside: the body is a thin-walled egg, so a point inside its
    wall is already within the margin — and the nearest-face-normal inside test misreads
    points whose nearest feature is an edge (it called a point 45 mm clear a collision)."""
    points = [p for item in items for p in item["points"]]
    if not points:
        return
    points = points[::max(1, len(points) // MAX_SWEEP_POINTS)]
    poses = [(p, r, y, z) for p in PITCHES for r in ROLLS for y in YAWS for z in LIFTS]

    def nearest(pts: list, matrix: Matrix) -> float:
        best = math.inf
        for point in pts:
            location, _, _, distance = body_tree.find_nearest(matrix @ point)
            if location is not None and distance < best:
                best = distance
        return best

    worst = None      # the pose where the add-ons are furthest inside what is allowed
    closest = None    # the add-ons' nearest approach overall, for the OK line
    for pose in poses:
        matrix = pose_matrix(*pose)
        mine = nearest(points, matrix)
        if closest is None or mine < closest[0]:
            closest = (mine, pose)
        if mine >= MOTION_MARGIN:
            continue
        standard = nearest(base_points, matrix)
        allowed = min(MOTION_MARGIN, standard - 0.5)
        if mine < allowed and (worst is None or allowed - mine > worst[0]):
            worst = (allowed - mine, pose, mine, standard)

    def where(pose: tuple) -> str:
        pitch, roll, yaw, lift = pose
        return f"pitch {pitch:+.0f}, roll {roll:+.0f}, yaw {yaw:+.0f}, lift {lift:+.0f} mm"

    if worst is not None:
        _, pose, mine, standard = worst
        report.fix(f"When the head moves ({where(pose)}) an add-on comes within {mine:.1f} mm "
                   f"of the body, where the standard head stays {standard:.1f} mm away. Keep "
                   "the lower part of the head close to the original shape.")
    elif closest is not None:
        report.ok(f"Swept {len(poses)} head poses: your add-ons never come closer to the body "
                  f"than the standard head does (nearest {closest[0]:.1f} mm, at {where(closest[1])})")


def base_sweep_points() -> list:
    """The standard head's lower half — where it meets the body — in world coordinates."""
    points = []
    for name in (BASE_SHELL, BASE_FACE):
        bm = world_bmesh(bpy.data.objects[name])
        points += [v.co.copy() for v in bm.verts if v.co.z < 10.0]
        bm.free()
    return points[::max(1, len(points) // 4000)]


# ── Building and exporting the result ─────────────────────────────────────────────────

def result_collection() -> bpy.types.Collection:
    coll = bpy.data.collections.get(RESULT_COLLECTION)
    if coll is None:
        coll = bpy.data.collections.new(RESULT_COLLECTION)
        bpy.context.scene.collection.children.link(coll)
    for obj in list(coll.objects):
        mesh = obj.data
        bpy.data.objects.remove(obj, do_unlink=True)
        if mesh is not None and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    return coll


def build_part(part: str, base_obj, addons: list, cuts: list, coll) -> bpy.types.Object:
    """Base + add-ons joined into one mesh, then every cut subtracted (exact booleans)."""
    mesh = bpy.data.meshes.new(f"{ROBOT}_{DESIGN}_{part}")
    bm = bmesh.new()
    for obj, weld in [(base_obj, False)] + [(a["obj"], True) for a in addons]:
        piece = world_bmesh(obj, weld=weld)
        temp = bpy.data.meshes.new("_piece")
        piece.to_mesh(temp)
        piece.free()
        bm.from_mesh(temp)
        bpy.data.meshes.remove(temp)
    bm.to_mesh(mesh)
    bm.free()
    result = bpy.data.objects.new(f"PRINT_{part}", mesh)
    coll.objects.link(result)

    # Each cut becomes a welded, world-space mesh first: a Text object handed straight to a
    # boolean is an open mesh, and the exact solver carves garbage out of an open cutter.
    cutters = []
    for i, cut in enumerate(cuts):
        piece = world_bmesh(cut["obj"], weld=True)
        cutter_mesh = bpy.data.meshes.new(f"_cutter{i}")
        piece.to_mesh(cutter_mesh)
        piece.free()
        cutter = bpy.data.objects.new(f"_cutter{i}", cutter_mesh)
        coll.objects.link(cutter)
        cutters.append(cutter)
        mod = result.modifiers.new(f"cut{i}", "BOOLEAN")
        mod.operation = "DIFFERENCE"
        mod.solver = "EXACT"
        mod.object = cutter
        mod.use_self = True
        mod.use_hole_tolerant = True
    if addons and not cuts:
        # Nothing to subtract, but let one exact union resolve the overlapping add-ons into
        # a single solid, so the weight is not counted twice where they overlap.
        mod = result.modifiers.new("merge", "BOOLEAN")
        mod.operation = "UNION"
        mod.solver = "EXACT"
        mod.operand_type = "COLLECTION"
        mod.collection = _empty_collection()
        mod.use_self = True
        mod.use_hole_tolerant = True
    if result.modifiers:
        depsgraph = bpy.context.evaluated_depsgraph_get()
        solid = bpy.data.meshes.new_from_object(result.evaluated_get(depsgraph))
        result.modifiers.clear()
        name = mesh.name
        result.data = solid
        bpy.data.meshes.remove(mesh)
        solid.name = name
    for cutter in cutters:
        cutter_mesh = cutter.data
        bpy.data.objects.remove(cutter, do_unlink=True)
        bpy.data.meshes.remove(cutter_mesh)
    return result


def _empty_collection() -> bpy.types.Collection:
    coll = bpy.data.collections.get("_reachy_empty")
    if coll is None:
        coll = bpy.data.collections.new("_reachy_empty")
    return coll


def export_stl(obj, path: str) -> None:
    for other in bpy.context.view_layer.objects:
        other.select_set(False)
    obj.hide_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=path, export_selected_objects=True, global_scale=1.0,
                          use_scene_unit=False, forward_axis="Y", up_axis="Z",
                          apply_modifiers=True, ascii_format=False)


def show_report(report: Report) -> str:
    text = bpy.data.texts.get(REPORT_TEXT) or bpy.data.texts.new(REPORT_TEXT)
    body = "\n".join(report.lines) + "\n"
    text.from_string(body)
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == "TEXT_EDITOR":
                area.spaces.active.text = text
                break
    print(body)
    return body


# ── Main ──────────────────────────────────────────────────────────────────────────────

def run(export: bool = True) -> dict:
    report = Report()
    report.lines.append(f"REACHY HEAD CHECK  -  {ROBOT} / {DESIGN}"
                        f"   (antennae {'kept' if KEEP_ANTENNAE else 'removed'})")

    if not re.fullmatch(r"R[1-9]", ROBOT) or not re.fullmatch(r"[A-Za-z0-9-]{1,40}", DESIGN):
        report.fix('Set ROBOT to your robot number (like "R3") and DESIGN to a short name '
                   'using letters, numbers and dashes, at the top of this script.')
    missing = [n for n in (BASE_SHELL, BASE_FACE, BODY) if bpy.data.objects.get(n) is None]
    if missing:
        report.fix(f"The starter file's parts are missing ({', '.join(missing)}). "
                   "Start again from reachy_head_starter.blend.")
        show_report(report)
        return {"passed": False, "report": report.lines}

    bases = {}
    for part, name in (("shell", BASE_SHELL), ("face", BASE_FACE)):
        bm = world_bmesh(bpy.data.objects[name])
        bases[part] = (BVHTree.FromBMesh(bm), volume_cm3(bm))
        bm.free()
    trees = keep_out_trees()
    body_bm = world_bmesh(bpy.data.objects[BODY])
    body_tree = BVHTree.FromBMesh(body_bm)
    body_bm.free()

    report.head("ADD-ONS")
    addons = [check_item(o, "addons", trees, bases, report)
              for o in collection_objects(ADD_COLLECTION)]
    if not collection_objects(ADD_COLLECTION):
        report.note(f'nothing in "{ADD_COLLECTION}"')
    report.head("CUTS")
    cuts = [check_item(o, "cuts", trees, bases, report)
            for o in collection_objects(CUT_COLLECTION)]
    if not collection_objects(CUT_COLLECTION):
        report.note(f'nothing in "{CUT_COLLECTION}"')
    addons = [a for a in addons if a]
    cuts = [c for c in cuts if c]

    report.head("HEAD MOVEMENT")
    if addons:
        sweep_motion(addons, base_sweep_points(), body_tree, report)
    else:
        report.note("no add-ons, so nothing new can hit the body")

    report.head("WEIGHT")
    coll = result_collection()
    built = {}
    for part, base_name in (("shell", BASE_SHELL), ("face", BASE_FACE)):
        part_addons = [a for a in addons if a["part"] == part]
        part_cuts = [c for c in cuts if c["part"] == part]
        if not part_addons and not part_cuts:
            if part == "face":
                report.note("face plate unchanged - print the standard s10_face_plate.stl")
                continue
        obj = build_part(part, bpy.data.objects[base_name], part_addons, part_cuts, coll)
        bm = world_bmesh(obj)
        grams = volume_cm3(bm) * PETG_G_PER_CM3
        closed = is_closed(bm)
        bm.free()
        built[part] = obj
        if part == "shell":
            line = f"back shell: {grams:.1f} g of {SHELL_MAX_G:.0f} g"
            (report.ok if grams <= SHELL_MAX_G else report.fix)(
                line if grams <= SHELL_MAX_G else line + " - make the add-ons smaller or hollow")
        else:
            added = grams - bases["face"][1] * PETG_G_PER_CM3
            line = f"face plate: {added:+.1f} g added, of {FACE_ADD_MAX_G:.0f} g allowed"
            (report.ok if added <= FACE_ADD_MAX_G else report.fix)(line)
        if not closed:
            report.note(f"the printed {part} has some open edges where parts meet. Slicers "
                        "cope with this; if yours complains, run 3D Print Toolbox > Make Manifold "
                        f"on PRINT_{part}.")

    report.head("RESULT")
    exported = []
    if report.failed:
        report.lines.append("  FAIL - fix every FIX line above and run it again. Nothing was exported.")
    elif export:
        if not bpy.data.filepath:
            report.fix("Save your .blend file first (File > Save As) - the STL files go next to it.")
            report.lines.append("  FAIL - nothing was exported.")
        else:
            folder = bpy.path.abspath("//export")
            os.makedirs(folder, exist_ok=True)
            for part, obj in built.items():
                path = os.path.join(folder, f"{ROBOT}_{DESIGN}_{part}.stl")
                export_stl(obj, path)
                exported.append(path)
            report.lines.append("  PASS - exported:")
            report.lines.extend(f"         {p}" for p in exported)
            report.lines.append("  Print the shell collar-down (open front edge on the bed), "
                                "PETG, 3 walls, 15% infill.")
    else:
        report.lines.append("  PASS")
    for obj in built.values():
        obj.hide_set(True)
    show_report(report)
    return {"passed": not report.failed, "report": report.lines, "exported": exported}


if __name__ == "__main__":
    run()
