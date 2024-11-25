from enum import Enum
from typing import Callable


class Job(str, Enum):
    TO_SQUARE: str = "to_square"
    TO_SQRT: str = "to_sqrt"


def sqrt_number(number: int) -> float:
    if number < 0:
        raise ValueError("You can't take the square root of a negative number.")

    return number ** 0.5


JOB_TO_FUNCTION: dict[str, Callable[[int], float]] = {
    Job.TO_SQUARE: lambda x: x ** 2,
    Job.TO_SQRT: lambda x: sqrt_number(x),
}
