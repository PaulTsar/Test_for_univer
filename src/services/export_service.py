import json
import csv
import xml.etree.ElementTree as ET
import yaml


from database_sqlite import PROJECT_DIR
from repositories.export_repository import get_students_for_export


def get_students_data():
    rows = get_students_for_export()

    students = []

    for row in rows:
        student = {
            "student_id": row[0],
            "full_name": row[1],
            "group": {
                "group_id": row[2],
                "name": row[3]
            }
        }

        students.append(student)

    return students


def export_to_json(students):
    output_dir = PROJECT_DIR / "out"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "data.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            students,
            file,
            ensure_ascii=False,
            indent=4
        )

    return file_path


def flatten_dict(data, prefix=""):
    result = {}

    for key, value in data.items():
        if prefix:
            column_name = prefix + "." + key
        else:
            column_name = key

        if isinstance(value, dict):
            nested_data = flatten_dict(value, column_name)
            result.update(nested_data)
        else:
            result[column_name] = value

    return result


def export_to_csv(students):
    output_dir = PROJECT_DIR / "out"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "data.csv"

    rows = []

    for student in students:
        rows.append(flatten_dict(student))

    columns = []

    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)

    with open(
        file_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        writer.writeheader()
        writer.writerows(rows)

    return file_path


def add_xml_elements(parent, data):
    for key, value in data.items():
        element = ET.SubElement(parent, key)

        if isinstance(value, dict):
            add_xml_elements(element, value)
        else:
            if value is not None:
                element.text = str(value)
            else:
                element.set("null", "true")


def export_to_xml(students):
    output_dir = PROJECT_DIR / "out"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "data.xml"

    root = ET.Element("records")

    for student in students:
        record = ET.SubElement(root, "record")
        add_xml_elements(record, student)

    tree = ET.ElementTree(root)

    ET.indent(tree, space="    ")

    tree.write(
        file_path,
        encoding="utf-8",
        xml_declaration=True
    )

    return file_path


def export_to_yaml(students):
    output_dir = PROJECT_DIR / "out"
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "data.yaml"

    with open(file_path, "w", encoding="utf-8") as file:
        yaml.safe_dump(
            students,
            file,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False
        )

    return file_path