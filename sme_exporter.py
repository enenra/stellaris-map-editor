import bpy
import os
import time

from .sme_importer import parse_line

def export_map_file(self, context):

    start = time.time()

    filepath = self.filepath
    entries = collect_map_info(context)

    if not os.path.isfile(filepath):
        lines = []

        for e in entries:
            lines.append(create_line(e))

        lines_merged = ""
        for l in lines:
            lines_merged += l + "\n"

        map_file = open(filepath, "w")
        map_file.write(lines_merged)


    if os.path.isfile(filepath):
        content = []
        with open(filepath) as file:
            lines = file.readlines()
            for line in lines:
                content.append(parse_line(line))
            file.close()

        l_index = 0
        for p in content:
            if p["type"] == "unsupported":
                p["processed"] = True
                l_index += 1
                continue

            for e in entries:
                if e["processed"]:
                    continue

                if p["type"] == "system" and e["type"] == "system":
                    if p["id"] != e["id"]:
                        continue
                    lines[l_index] = update_line(lines[l_index], p, e)
                    e["processed"] = True
                    p["processed"] = True
                    break

                elif p["type"] == "nebula" and e["type"] == "nebula":
                    if p["name"] != e["name"]:
                        continue
                    lines[l_index] = update_line(lines[l_index], p, e)
                    e["processed"] = True
                    p["processed"] = True
                    break

                elif p["type"] == "add_hyperlane" and e["type"] == "add_hyperlane":
                    if (p["from"] == e["from"]) and (p["to"] == e["to"]):
                        e["processed"] = True
                        p["processed"] = True
                        break

            l_index += 1

        # Removing lines whose objects don't exist in Blender
        for p in content:
            if p["processed"]:
                continue

            for l in lines:
                parsed = parse_line(l)

                if p["type"] == "system" and parsed["type"] == "system":
                    if p["id"] == parsed["id"]:
                        print(f"Removed line (does not exist in blend file): {l[:-1]}")
                        lines.remove(l)
                        break

                elif p["type"] == "nebula" and parsed["type"] == "nebula":
                    if p["name"] == parsed["name"]:
                        print(f"Removed line (does not exist in blend file): {l[:-1]}")
                        lines.remove(l)
                        break

                elif p["type"] == "add_hyperlane" and parsed["type"] == "add_hyperlane":
                    if (p["from"] == parsed["from"]) and (p["to"] == parsed["to"]):
                        print(f"Removed line (does not exist in blend file): {l[:-1]}")
                        lines.remove(l)
                        break


        for e in entries:
            if e["processed"]:
                continue
            lines.insert(-1, "\t" + create_line(e) + "\n")

        lines_merged = ""
        for l in lines:
            lines_merged += l

        map_file = open(filepath.split(".txt")[0] + "_new.txt", "w")
        map_file.write(lines_merged)


    systems = 0
    nebulae = 0
    hyperlanes = 0
    for e in entries:
        if e["type"] == "system":
            systems += 1
        elif e["type"] == "nebula":
            nebulae += 1
        elif e["type"] == "add_hyperlane":
            hyperlanes += 1

    print(f"Exported {len(entries)} entries: {systems} systems, {nebulae} nebulae, {hyperlanes} hyperlanes")

    end = time.time()
    print(f"Time: {round(end-start, 1)}s")

    return {'FINISHED'}


def collect_map_info(context) -> list:
    objects = []

    id_checker = []
    for obj in context.scene.objects:
        if obj.sme.object_type == "none":
            continue

        entry = {}
        entry["type"] = obj.sme.object_type
        entry["processed"] = False

        if obj.sme.object_type == "system":
            entry["id"] = obj.sme.sme_id
            id_checker.append(obj.sme.sme_id)
            entry["name"] = obj.name.split(".")[0]
            entry["x"] = int(round((obj.location.x * 10) * -1, 0))
            entry["y"] = int(round((obj.location.y * 10) * -1, 0))

        elif obj.sme.object_type == "nebula":
            entry["name"] = obj.name.split(".")[0]
            entry["x"] = int(round((obj.location.x * 10) * -1, 0))
            entry["y"] = int(round((obj.location.y * 10) * -1, 0))
            entry["radius"] = int(round(obj.scale.x * 10, 0))

        elif obj.sme.object_type == "add_hyperlane":
            if obj.modifiers["Hyperlane"]["Socket_4"] is None or obj.modifiers["Hyperlane"]["Socket_5"] is None:
                print(f"Error: Hyperlane '{obj.name}' is missing either From or To.")
                continue

            entry["from"] = obj.modifiers["Hyperlane"]["Socket_4"].sme.sme_id
            entry["to"] = obj.modifiers["Hyperlane"]["Socket_5"].sme.sme_id

        objects.append(entry)

    seen = set()
    duplicates = []

    for i in id_checker:
        if i in seen:
            duplicates.append(i)
        else:
            seen.add(i)

    if len(duplicates) > 0:
        print(f"Error: Duplicate IDs detected: {duplicates}")

    return objects


def update_line(line, parsed, entry) -> str:
    if parsed["type"] == "system":
        newline = replace_line(line, parsed, entry, "name")
        newline = replace_line(newline, parsed, entry, "id")
        newline = replace_line(newline, parsed, entry, "x")
        newline = replace_line(newline, parsed, entry, "y")

    elif parsed["type"] == "nebula":
        newline = replace_line(line, parsed, entry, "name")
        newline = replace_line(newline, parsed, entry, "radius")
        newline = replace_line(newline, parsed, entry, "x")
        newline = replace_line(newline, parsed, entry, "y")

    return newline


def replace_line(line, p, e, key) -> str:
    parsed = str(p[key])
    entry = str(e[key])
    return line.replace(f" {key} = {parsed} ", f" {key} = {entry} ")


def create_line(entry) -> str:
    line = ""

    if entry["type"] == "system":
        line = 'system = { id = "' + str(entry["id"]) + '" name = "' + str(entry["name"]) + '" position = { x = ' + str(entry["x"]) + ' y = ' + str(entry["y"]) + ' } }'

    elif entry["type"] == "nebula":
        line = 'nebula = { name = "' + str(entry["name"]) + '" position = { x = ' + str(entry["x"]) + ' y = ' + str(entry["y"]) + ' } radius = ' + str(entry["radius"]) + ' }'

    elif entry["type"] == "add_hyperlane":
        line = 'add_hyperlane = { from = "' + str(entry["from"]) + '" to = "' + str(entry["to"]) + '" }'

    return line