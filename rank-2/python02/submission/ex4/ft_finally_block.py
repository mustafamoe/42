class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system() -> None:
    print("=== Garden Watering System ===")
    print("Testing valid plants...")
    print("Opening watering system")
    try:
        for plant_name in ("Tomato", "Lettuce", "Carrots"):
            water_plant(plant_name)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
        return
    finally:
        print("Closing watering system")
    print("Testing invalid plants...")
    print("Opening watering system")
    try:
        for plant_name in ("Tomato", "lettuce", "Carrots"):
            water_plant(plant_name)
    except PlantError as error:
        print(f"Caught PlantError: {error}")
        print(".. ending tests and returning to main")
    finally:
        print("Closing watering system")
    print("Cleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
