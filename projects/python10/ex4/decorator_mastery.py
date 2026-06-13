from collections.abc import Callable
from functools import wraps
from time import perf_counter, sleep
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start_time = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = perf_counter() - start_time
            print(f"Spell completed in {duration:.3f} seconds")

    return wrapper


def power_validator(
    min_power: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get("power", args[-1] if args else None)
            if not isinstance(power, int) or power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(
    max_attempts: int,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        return (
                            "Spell casting failed after "
                            f"{max_attempts} attempts"
                        )
                    print(
                        "Spell failed, retrying... "
                        f"(attempt {attempt + 1}/{max_attempts})"
                    )
            return "Spell casting failed after 0 attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    sleep(0.1)
    return "Fireball cast!"


@retry_spell(3)
def unstable_spell() -> str:
    raise RuntimeError("unstable spell")


@power_validator(10)
def lightning(target: str, power: int) -> str:
    return f"Lightning hits {target} with {power} power"


def main() -> None:
    guild = MageGuild()

    print("Testing spell timer...")
    print(f"Result: {fireball()}")

    print("Testing retrying spell...")
    print(unstable_spell())
    print(lightning("Tower", 12))

    print("Testing MageGuild...")
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("Jo"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
