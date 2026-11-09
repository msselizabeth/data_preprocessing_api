import secrets
from .json_validator import get_selected_values
from pydantic import JsonValue


def mask_json(
    data: dict[str, JsonValue], paths: list[str]
) -> tuple[dict[str, JsonValue], dict[str, str], dict[str, str]]:
    selected_values = get_selected_values(data, paths)

    masked_data = data.copy()
    mappings = {}  # all exising placeholders and their values
    field_placeholders = {}  # path -> placeholder

    operation_id = secrets.token_hex(16)

    for key, value in selected_values.items():
        if value is None or value.strip() == "":
            continue

        field_name = key[1:]

        if value not in mappings.values():
            placeholder = f"{field_name}_{operation_id}"

            mappings[placeholder] = value
            field_placeholders[key] = placeholder
            masked_data[field_name] = placeholder
        else:
            matched_key = next((k for k, v in mappings.items() if v == value), None)
            masked_data[field_name] = matched_key
            field_placeholders[key] = matched_key

    return (masked_data, mappings, field_placeholders)


def restore_json(
    masked_data: dict[str, JsonValue], mappings: dict[str, str]
) -> dict[str, JsonValue]:

    restored_data = masked_data.copy()

    for key, value in masked_data.items():
        if isinstance(value, str) and value in mappings:
            restored_data[key] = mappings[value]

    return restored_data


if __name__ == "__main__":
    data = {
        "name": "Elizabeth",
        "email": None,
        "orders_count": 5,
        "last_name": "Sheremet",
        "empty_test": "",
        "second_name_test": "Elizabeth",
    }
    paths = ["/name", "/email", "/last_name", "/empty_test", "/second_name_test"]

    masked_date, mappings, field_placeholders_dict = mask_json(data, paths)
    print(f"Masking Result: {masked_date}\n")
    print(f"Mappings: {mappings}\n")
    print(f"Paths -> Placeholders Dict: {field_placeholders_dict}\n")

    restored = restore_json(masked_data=masked_date, mappings=mappings)
    print(f"Original data: {data}\n")
    print(f"Restored data: {restored}\n")
    print(f"Original == Restired: {restored == data}")
