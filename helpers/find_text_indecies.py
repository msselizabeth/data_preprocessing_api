from schemas.clean_data import CleanDataRequest


def find_text_index(text: str, add_values: list[str]) -> list[tuple[int, int, str]]:

    results = []

    for val in add_values:

        if not val.strip():
            raise ValueError("Additional values must not be blank.")

        next_idx = 0

        while True:
            found_idx = text.find(val, next_idx)

            if found_idx == -1:
                break

            end_idx = found_idx + len(val)
            next_idx = found_idx + 1

            results.append((found_idx, end_idx, val))

    return results


if __name__ == "__main__":
    request = CleanDataRequest(
        text="Elizabeth emailed Elizabeth.",
        additional_values=[" "],
    )

    print(request.additional_values)
    print(find_text_index(request.text, request.additional_values))
