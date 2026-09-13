class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height)
        self.set_age(age)

    def show(self) -> None:
        print(f"{self._name}: {self._height:.1f}cm, {self._age} days old")

    def grow(self, amount: float) -> None:
        self.set_height(round(self._height + amount, 1))

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


if __name__ == "__main__":
    rose = Plant("Rose", 15.0, 10)

    print("=== Garden Security System ===")
    print("Plant created: ", end="")
    rose.show()

    if rose.set_height(25):
        print("Height updated: 25cm")
    else:
        print("Height update rejected")

    if rose.set_age(30):
        print("Age updated: 30 days")
    else:
        print("Age update rejected")

    if rose.set_height(-5):
        print("Height updated: -5cm")
    else:
        print("Height update rejected")

    if rose.set_age(-3):
        print("Age updated: -3 days")
    else:
        print("Age update rejected")

    print("Current state: ", end="")
    rose.show()
