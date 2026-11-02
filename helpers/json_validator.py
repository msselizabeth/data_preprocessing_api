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


if __name__ == "__main__":
    data = {"name": "Elizabeth", "email": None, "orders_count": 5}
    paths = ["/name", "/email"]

    print(f"Input: {data}")

    result = get_selected_values(data, paths)
    print(f"Result: {result}")
