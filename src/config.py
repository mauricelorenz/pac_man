import sys
from typing import Any, List

from pydantic import (
    BaseModel,
    Field,
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


def default_levels() -> List[Level]:
    return [Level.model_construct()]


class Config(BaseModel):
    highscore_filename: str = "highscore.json"
    levels: List[Level] = Field(default_factory=default_levels)
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90

    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        for field in cls.model_fields:
            if field not in data:
                if field != "levels":
                    fallback = repr(cls.model_fields[field].default)
                else:
                    fallback = "one default level"
                print(
                    f"Missing key '{field}'. Falling back to "
                    f"{fallback}", file=sys.stderr
                )
        return data

    @field_validator(
        "lives", "pacgum", "points_per_pacgum", "points_per_super_pacgum",
        "points_per_ghost", "level_max_time", mode="before"
    )
    @classmethod
    def validate_positive(cls, v: Any, info: ValidationInfo) -> Any:
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

    @field_validator("seed", mode="before")
    @classmethod
    def validate_seed(cls, v: Any) -> Any:
        if isinstance(v, int) and not isinstance(v, bool):
            return v
        default = cls.model_fields["seed"].default
        print(
            f"Invalid value for key 'seed' (int): {v!r}. "
            f"Falling back to {default!r}",
            file=sys.stderr
        )
        return default

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def validate_filename(cls, v: Any) -> Any:
        if (
            isinstance(v, str) and v == v.strip() and "/" not in v
            and "\\" not in v and v.endswith(".json") and v != ".json"
        ):
            return v
        default = cls.model_fields["highscore_filename"].default
        print(
            f"Invalid value for key 'highscore_filename' "
            f"(plain *.json filename): {v!r}. Falling back to {default!r}",
            file=sys.stderr
        )
        return default

    @field_validator("levels", mode="before")
    @classmethod
    def validate_levels(cls, v: Any) -> Any:
        if (not v or not isinstance(v, list)):
            print(
                f"Invalid value for key 'levels' (non-empty list): {v!r}. "
                "Falling back to one default level",
                file=sys.stderr
            )
            return default_levels()
        result: List[Any] = []
        for item in v:
            if isinstance(item, dict):
                result.append(item)
            else:
                print(
                    f"Invalid member value for key 'levels' (dict): "
                    f"{item!r}. Falling back to default level",
                    file=sys.stderr
                )
                result.append(Level.model_construct())
        return result
