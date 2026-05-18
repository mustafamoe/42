class Plant:
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        growth_rate: float = 0.0,
    ) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self._growth_rate = growth_rate
        self.set_height(height)
        self.set_age(age)

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._age} days old")

    def grow(self, days: int = 1) -> None:
        self.set_height(round(self._height + self._growth_rate * days, 1))

    def age(self, days: int = 1) -> None:
        self.set_age(self._age + days)

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = height
        return True

    def set_age(self, age: int) -> bool:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            return False
        self._age = age
        return True


class Flower(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        color: str,
        growth_rate: float = 0.0,
    ) -> None:
        super().__init__(name, height, age, growth_rate)
        self._color = color
        self._bloomed = False

    def bloom(self) -> None:
        self._bloomed = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        trunk_diameter: float,
        growth_rate: float = 0.0,
    ) -> None:
        super().__init__(name, height, age, growth_rate)
        self._trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height:.1f}cm long and {self._trunk_diameter:.1f}cm wide."
        )

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter:.1f}cm")


class Vegetable(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        harvest_season: str,
        growth_rate: float = 0.0,
    ) -> None:
        super().__init__(name, height, age, growth_rate)
        self._harvest_season = harvest_season
        self._nutritional_value = 0

    def grow(self, days: int = 1) -> None:
        super().grow(days)
        self._nutritional_value += days

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


if __name__ == "__main__":
    rose = Flower("Rose", 15.0, 10, "red")
    oak = Tree("Oak", 200.0, 365, 5.0)
    tomato = Vegetable("Tomato", 5.0, 10, "April", 2.1)

    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("=== Tree")
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("=== Vegetable")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    tomato.grow(20)
    tomato.age(20)
    tomato.show()
