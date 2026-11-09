from services.export_service import (
    get_students_data,
    export_to_json,
    export_to_csv,
    export_to_xml,
    export_to_yaml
)


def main():
    students = get_students_data()

    json_path = export_to_json(students)
    csv_path = export_to_csv(students)
    xml_path = export_to_xml(students)
    yaml_path = export_to_yaml(students)

    print("Данные сохранены:")
    print(json_path)
    print(csv_path)
    print(xml_path)
    print(yaml_path)


if __name__ == "__main__":
    main()