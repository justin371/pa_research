"""Search the local, curated PA visual reference registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "knowledge" / "brooks_visual_examples.json"
REQUIRED_FIELDS = {
    "id": str,
    "title": str,
    "concepts": list,
    "source_url": str,
    "page": int,
    "visual_status": str,
    "contrast_note": str,
    "usage": str,
}
IMAGE_FIELDS = ("local_image_paths", "image_paths", "image_path")


def _validate_entry(entry, index):
    if not isinstance(entry, dict):
        raise ValueError(f"entry {index} must be an object")
    for field, expected in REQUIRED_FIELDS.items():
        if field not in entry or not isinstance(entry[field], expected):
            raise ValueError(f"entry {index} field {field!r} has the wrong type")
    if not entry["id"].strip():
        raise ValueError(f"entry {index} id must be non-empty")
    if not all(isinstance(concept, str) for concept in entry["concepts"]):
        raise ValueError(f"entry {index} concepts must contain only strings")
    if isinstance(entry["page"], bool) or entry["page"] <= 0:
        raise ValueError(f"entry {index} page must be a positive integer")
    source_url = entry["source_url"]
    if not source_url.lower().startswith("https://"):
        raise ValueError(f"entry {index} source_url must be an https URL")
    authority = source_url[8:].split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if not authority or any(char.isspace() for char in authority):
        raise ValueError(f"entry {index} source_url must be an https URL")
    for field in IMAGE_FIELDS:
        if field not in entry:
            continue
        value = entry[field]
        if field == "image_path":
            valid = isinstance(value, str)
        else:
            valid = isinstance(value, list) and all(isinstance(item, str) for item in value)
        if not valid:
            raise ValueError(f"entry {index} field {field!r} has the wrong type")


def _validate_entries(entries):
    if not isinstance(entries, list):
        raise ValueError("registry entries must be a JSON array")
    ids = set()
    for index, entry in enumerate(entries):
        _validate_entry(entry, index)
        if entry["id"] in ids:
            raise ValueError(f"duplicate entry id: {entry['id']}")
        ids.add(entry["id"])
    return entries


def load_registry(path=DEFAULT_REGISTRY):
    """Load and validate a JSON array, or an object containing ``entries``."""
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read registry {path}: {exc}") from exc
    if isinstance(document, dict):
        document = document.get("entries")
    return _validate_entries(document)


def search_registry(entries, query=None):
    """Return matching entries in registry order; an empty query returns all."""
    entries = _validate_entries(entries)
    if query is None or not str(query).strip():
        return list(entries)
    if not isinstance(query, str):
        raise TypeError("query must be text")
    tokens = query.casefold().split()
    matches = []
    for entry in entries:
        haystack = " ".join(
            [entry["id"], entry["title"], entry["contrast_note"], *entry["concepts"]]
        ).casefold()
        if all(token in haystack for token in tokens):
            matches.append(entry)
    return matches


def _declared_image_paths(entry):
    paths = []
    for field in IMAGE_FIELDS:
        value = entry.get(field)
        if isinstance(value, str):
            paths.append(value)
        elif isinstance(value, list):
            paths.extend(value)
    return paths


def _available_image_paths(entry, registry_path):
    root = Path(registry_path).resolve().parent
    available = []
    for raw_path in _declared_image_paths(entry):
        path = Path(raw_path)
        candidate = path if path.is_absolute() else root / path
        if candidate.is_file():
            resolved = str(candidate.resolve())
            if resolved not in available:
                available.append(resolved)
    return available


def _output_entries(entries, registry_path):
    output = []
    for entry in entries:
        item = dict(entry)
        if any(field in entry for field in IMAGE_FIELDS):
            item["local_image_paths"] = _available_image_paths(entry, registry_path)
        output.append(item)
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", help="case-insensitive text to find")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args(argv)
    try:
        entries = search_registry(load_registry(args.registry), args.query)
        result = _output_entries(entries, args.registry)
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
