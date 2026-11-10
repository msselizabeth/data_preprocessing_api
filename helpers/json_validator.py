from pydantic import JsonValue

def get_selected_values(data: dict [str, JsonValue], paths: list[str]) -> dict[str, str | None]:
    replace_dict = {}
    for path in paths:
        field_name = path[1:]
        if field_name not in data:
            raise ValueError(f"The field: {path} does not exist.")

        value = data[field_name]
        if not isinstance(value, str) and value is not None:
            raise ValueError(f"The field: {path} must contain string value or None.")

        replace_dict[path] = value

    
    return replace_dict


def validate_restore_data(
    data: dict[str, JsonValue],
    field_placeholders: dict[str, str],
    partial: bool = False,
) -> None:
    
    match_count = 0

    for path, expected_placeholder in field_placeholders.items():
        field_name = path[1:]

        if field_name not in data:
            if partial:
                continue
            raise ValueError(f"Required field at path '{path}' is missing.")

        if data[field_name] != expected_placeholder:
                raise ValueError(f"Value at '{path}' does not match the expected placeholder.")
        
        match_count += 1

    if match_count == 0:
        raise ValueError("No matching fields to restore")



if __name__ == "__main__":
    field_placeholders = {
        "/name": "name_operationA",
        "/email": "email_operationA",
    }

    # 1. Full document — OK
    # data = {"name": "name_operationA", "email": "email_operationA"}
    # partial = False

    # 2. Missing email — ERROR
    # data = {"name": "name_operationA"}
    # partial = False

    # 3. Partial document — OK
    # data = {"name": "name_operationA"}
    # partial = True

    # 4. Placeholder from another operation — ERROR
    data = {"name": "name_operationB"}
    partial = True

    # 5. No fields to restore — ERROR
    # data = {}
    # partial = True

    try:
        validate_restore_data(data, field_placeholders, partial)
        print("OK")
    except ValueError as exc:
        print(f"ERROR: {exc}")

    # TODO: Revisit these cases when learning pytest.
    # Add automated tests, including checks that inputs remain unchanged.