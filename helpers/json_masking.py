from .json_validator import get_selected_values
from pydantic import JsonValue


def mask_json(
    data: dict[str, JsonValue], paths: list[str]
) -> tuple[dict[str, JsonValue], dict[str, str]]:
    selected_values = get_selected_values(data, paths)

    masked_data = data.copy()
    mappings = {}
    val_counter = 1

    for key, value in selected_values.items():
        if value is None:
            continue

        if value not in mappings.values():
            placeholder = f"<VALUE_{val_counter}>"

            while placeholder in data.values():
                val_counter += 1
                placeholder = f"<VALUE_{val_counter}>"

            mappings[placeholder] = value
            masked_data[key[1:]] = placeholder
            val_counter += 1

        else:
            matched_key = next((k for k, v in mappings.items() if v == value), None)
            masked_data[key[1:]] = matched_key

    return (masked_data, mappings)


def restore_json(
    masked_data: dict[str, JsonValue], mappings: dict[str, str]
) -> dict[str, JsonValue]:

    restored_data = masked_data.copy()

    for key, value in masked_data.items():
        if isinstance(value, str) and value in mappings:
            restored_data[key] = mappings[value]

    return restored_data


# if __name__ == "__main__":
    # data = {
    #     "name": "Elizabeth",
    #     "email": None,
    #     "orders_count": 5,
    #     "last_name": "Sheremet",
    #     "empty_test": "",
    #     "second_name_test": "Elizabeth"
    # }
    # paths = ["/name", "/email", "/last_name", "/empty_test", "/second_name_test"]

    # data = {
    #     "name": "Elizabeth",
    #     "note": "<VALUE_1>",
    #     "second_name": "Elizabeth",
    # }
    # paths = ["/name", "/second_name"]

    # masked_date, mappings = mask_json(data, paths)
    # print(f"Masking Result: {masked_date}")
    # print(f"mappings: {mappings}")

    # restored = restore_json(masked_data=masked_date, mappings=mappings)

    # print(f"Original data: {data}")
    # print(f"Restored data: {restored}")

    # print(restored == data)
