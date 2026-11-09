import sys
from typing import Any, List

from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator,
    model_validator,
)


class Level(BaseModel):
    width: int = 20
    height: int = 15

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        for field in cls.model_fields:
            if field not in data:
                print(
                    f"Missing key '{field}'. Falling back to "
                    f"{cls.model_fields[field].default!r}", file=sys.stderr
                )
        return data

    @field_validator("width", "height", mode="before")
    @classmethod
    def validate_field(cls, v: Any, info: ValidationInfo) -> Any:
        name = info.field_name
        if name is None:
            return v
        if isinstance(v, int) and not isinstance(v, bool) and v > 0:
            return v
        default = cls.model_fields[name].default
        print(
            f"Invalid value for key '{name}' (int > 0): {v!r}. "
            f"Falling back to {default!r}",
            file=sys.stderr
        )
        return default


class Config(BaseModel):
    highscore_filename: str = "highscore.json"
    levels: List[Level]
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90
