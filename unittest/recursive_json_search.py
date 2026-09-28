"""Recursively search JSON data while enforcing field access permissions."""

from policy import POLICY


def json_search(key, input_object, role=None):
    """Return all accessible matches as single-key dictionaries.

    Fields absent from POLICY are public. Protected fields require an explicitly
    allowed role, so a missing or invalid role cannot read them. Container values
    are copied with inaccessible fields removed, including nested fields.
    """
    def can_read(field):
        return field not in POLICY or role in POLICY[field]

    if not can_read(key):
        return []

    def filter_value(value):
        if isinstance(value, dict):
            return {
                field: filter_value(child)
                for field, child in value.items()
                if can_read(field)
            }
        if isinstance(value, list):
            return [filter_value(child) for child in value]
        return value

    results = []

    def search(value):
        if isinstance(value, dict):
            for field, child in value.items():
                if not can_read(field):
                    continue
                if field == key:
                    results.append({field: filter_value(child)})
                search(child)
        elif isinstance(value, list):
            for child in value:
                search(child)

    search(input_object)
    return results
