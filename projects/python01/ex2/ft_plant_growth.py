class Plant:
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        daily_growth: float,
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age
        self.daily_growth = daily_growth

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.age_days} days old")

    def grow(self) -> None:
        self.height = round(self.height + self.daily_growth, 1)

    def age(self) -> None:
        self.age_days += 1


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30, 0.8)
    starting_height = rose.height

    print("=== Garden Plant Growth ===")
    rose.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()

    weekly_growth = round(rose.height - starting_height, 1)
    print(f"Growth this week: {weekly_growth:.1f}cm")
