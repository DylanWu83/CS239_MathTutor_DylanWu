from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, ValidationError

_JSON_FENCE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_JSON_OBJECT = re.compile(r"\{.*\}", re.DOTALL)


def parse_model(raw: Any, model: type[BaseModel]) -> BaseModel:
    if isinstance(raw, model):
        return raw
    if isinstance(raw, dict):
        return model.model_validate(raw)
    text = getattr(raw, "raw", None) or str(raw)
    payload = _nullify(_extract_json(text))
    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(f"Could not parse {model.__name__} from model output:\n{text}") from exc


def _nullify(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _nullify(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_nullify(item) for item in value]
    if value in ("null", "None", "none", ""):
        return None
    return value


def _extract_json(text: str) -> dict[str, Any]:
    fenced = _JSON_FENCE.search(text)
    blob = fenced.group(1) if fenced else None
    if blob is None:
        match = _JSON_OBJECT.search(text)
        if not match:
            raise ValueError(f"No JSON object found in:\n{text}")
        blob = match.group(0)
    try:
        return json.loads(blob)
    except json.JSONDecodeError as exc:
        if exc.msg != "Invalid \\escape":
            raise
        return json.loads(_escape_invalid_json_escapes(blob))


def _escape_invalid_json_escapes(blob: str) -> str:
    escaped: list[str] = []
    in_string = False
    index = 0
    valid_escapes = '"\\/bfnrtu'

    while index < len(blob):
        character = blob[index]
        if in_string and character == "\\" and index + 1 < len(blob):
            following = blob[index + 1]
            if following in valid_escapes:
                escaped.extend((character, following))
            else:
                escaped.extend(("\\\\", following))
            index += 2
            continue
        if character == '"':
            in_string = not in_string
        escaped.append(character)
        index += 1

    return "".join(escaped)
