import bpy
import os
import time

TEST_FILE = "C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\281990\\2791119024\\map\\setup_scenarios\\lotor_map_large.txt"

def import_map_file(self, context, filepath):

    start = time.time()

    with open(filepath) as file:
        lines = file.readlines()

        contents = []
        for line in lines:
            contents.append(parse_line(line))

    progress = time.time()

    system_count = 0
    nebula_count = 0
    hyperlane_count = 0
    for content in contents:
        if content["type"] == "unsupported":
            continue
        if content["type"] == "system":
            system_count += 1
        elif content["type"] == "nebula":
            nebula_count += 1
        elif content["type"] == "add_hyperlane":
            hyperlane_count += 1

    print(f"-------------------------------------------------- Importing Systems & Nebulae ({round(progress-start,1)}s)")

    systems_processed = 0
    nebulae_processed = 0

    id_dict = {}
    for content in contents:
        if content["type"] == "unsupported":
            continue

        if content["type"] == "system":
            id_dict[content["id"]] = create_system(content["name"], content["id"], content["x"], content["y"])
            systems_processed += 1

        elif content["type"] == "nebula":
            create_nebula(content["name"], content["x"], content["y"], content["radius"])
            nebulae_processed += 1

        print(f"Processed: Systems: {systems_processed}/{system_count} Nebulae: {nebulae_processed}/{nebula_count}", end="\r")

    print("")
    progress = time.time()
    print(f"-------------------------------------------------- Importing Hyperlanes ({round(progress-start,1)}s)")

    result = []
    hyperlanes_processed = 0
    for content in contents:
        if content["type"] == "unsupported":
            continue
        if content["type"] == "add_hyperlane":
            output = create_hyperlane(id_dict, content["from"], content["to"])
            if output is not None:
                result.append(output)
            hyperlanes_processed += 1

        print(f"Processed: Hyperlanes: {hyperlanes_processed}/{hyperlane_count}", end="\r")

    for l in result:
        print(l)

    print("")
    end = time.time()
    print(f"Time: {round(end-start, 1)}s")

    return {'FINISHED'}


def parse_line(line):

    content = {}

    # Cap off comments
    if "#" in line:
        line = line.split("#")[0]

    # No processing for anything else atm.
    if line.strip().startswith("system"):
        content["type"] = "system"
    elif line.strip().startswith("nebula"):
        content["type"] = "nebula"
    elif line.strip().startswith("add_hyperlane"):
        content["type"] = "add_hyperlane"
    else:
        content["type"] = "unsupported"

    if content["type"] == "system":
        content["id"] = int(line.split("id")[1].split('"')[1].strip())
        content["name"] = line.split("name")[1].split('"')[1]

        position = line.split("position")[1].split("{")[1].split("}")[0]
        content["x"] = int(position.split("x")[1].split("=")[1].split("y")[0].strip())
        content["y"] = int(position.split("y")[1].split("=")[1].strip())

    elif content["type"] == "nebula":
        content["name"] = line.split("name")[1].split('"')[1]

        position = line.split("position")[1].split("{")[1].split("}")[0]
        content["x"] = int(position.split("x")[1].split("=")[1].split("y")[0].strip())
        content["y"] = int(position.split("y")[1].split("=")[1].strip())

        content["radius"] = int(line.split("radius")[1].split("=")[1].split("}")[0].split("position")[0].strip())

    elif content["type"] == "add_hyperlane":
        content["from"] = int(line.split("from")[1].split('"')[1])
        content["to"] = int(line.split("to")[1].split('"')[1])

    content["processed"] = False

    return content


def create_system(name="System", id=None, x=0.0, y=0.0):

    if x != 0.0:
        x = (x / 10)*-1
    if y != 0.0:
        y = (y / 10)*-1

    bpy.ops.object.metaball_add(type='BALL', radius=2, enter_editmode=False, align='WORLD', location=(x, y, 0), scale=(1, 1, 1))
    system = bpy.context.active_object

    system.name = name
    system.scale = (0.1, 0.1, 0.1)

    system.sme.object_type = "system"

    if id is not None:
        system.sme.sme_id = id

    return system


def create_nebula(name="Nebula", x=0.0, y=0.0, radius=10.0):

    if x != 0.0:
        x = (x / 10)*-1
    if y != 0.0:
        y = (y / 10)*-1

    bpy.ops.object.metaball_add(type='BALL', radius=2, enter_editmode=False, align='WORLD', location=((x / 10)*-1, (y / 10)*-1, 0), scale=(1, 1, 1))
    nebula = bpy.context.active_object

    nebula.name = name
    nebula.scale = (radius / 10, radius / 10, radius / 10)
    nebula.display_type = 'WIRE'

    nebula.sme.object_type = "nebula"

    return nebula


def create_hyperlane(ids=None, hyperlane_from=None, hyperlane_to=None) -> str:

    bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    hyperlane = bpy.context.active_object

    # In theory it should be faster by avoiding the operator but I had trouble getting this to work

    # curve_data = bpy.data.curves.new('myCurve', type='CURVE')
    # curve_data.dimensions = '3D'
    # curve_data.resolution_u = 0

    # polyline = curve_data.splines.new('POLY')
    # polyline.points.add(2)

    # hyperlane = bpy.data.objects.new('myCurve', curve_data)
    # bpy.context.scene.objects.link(hyperlane)

    if not "Hyperlane" in bpy.data.node_groups:
        append_geo_nodes()

    modifier = hyperlane.modifiers.new("Hyperlane", "NODES")
    modifier.node_group = bpy.data.node_groups["Hyperlane"]

    if ids is not None:
        obj_from = None
        if hyperlane_from in ids:
            obj_from = ids[hyperlane_from]

        obj_to = None
        if hyperlane_to in ids:
            obj_to = ids[hyperlane_to]

        if obj_from is not None and obj_to is not None:
            hyperlane.sme.object_type = "add_hyperlane"
            hyperlane.name = f"Hyperlane ({obj_from.name} - {obj_to.name})"

            modifier["Socket_4"] = obj_from
            modifier["Socket_5"] = obj_to

        else:
            status_from = "Found"
            if obj_from is None:
                status_from = "Not Found"
            status_to = "Found"
            if obj_to is None:
                status_to = "Not Found"

            return f"Error: Hyperlane Issue: {hyperlane_from} ({status_from}) - {hyperlane_to} ({status_to})"

    else:
        hyperlane.sme.object_type = "add_hyperlane"
        hyperlane.name = "Hyperlane"


def append_geo_nodes():
    path = os.path.dirname(__file__) + "\\assets.blend"

    with bpy.data.libraries.load(path, link=True) as (data_from, data_to):
        data_to.node_groups = data_from.node_groups