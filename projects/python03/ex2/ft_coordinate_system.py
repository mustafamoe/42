import math


Coordinate = tuple[float, float, float]


def get_player_pos() -> Coordinate:
    while True:
        raw_coordinates = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )
        parts = raw_coordinates.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2])
        except ValueError as error:
            parameter = str(error).split("'")[1]
            print(f"Error on parameter '{parameter}': {error}")
            continue
        return (x, y, z)


def get_distance(first: Coordinate, second: Coordinate) -> float:
    return math.sqrt(
        (second[0] - first[0]) ** 2
        + (second[1] - first[1]) ** 2
        + (second[2] - first[2]) ** 2
    )


def main() -> None:
    print("=== Game Coordinate System ===")
    print("Get a first set of coordinates")
    first_position = get_player_pos()
    print(f"Got a first tuple: {first_position}")
    print(
        f"It includes: X={first_position[0]}, "
        f"Y={first_position[1]}, Z={first_position[2]}"
    )
    print(
        "Distance to center: "
        f"{round(get_distance((0.0, 0.0, 0.0), first_position), 4)}"
    )

    print("Get a second set of coordinates")
    second_position = get_player_pos()
    print(
        "Distance between the 2 sets of coordinates: "
        f"{round(get_distance(first_position, second_position), 4)}"
    )


if __name__ == "__main__":
    main()
