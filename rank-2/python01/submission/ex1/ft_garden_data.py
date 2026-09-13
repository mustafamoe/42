class Plant:
    name: str
    height: int
    age: int

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


if __name__ == "__main__":
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.age = 30

    sunflower = Plant()
    sunflower.name = "Sunflower"
    sunflower.height = 80
    sunflower.age = 45

    cactus = Plant()
    cactus.name = "Cactus"
    cactus.height = 15
    cactus.age = 120

    print("=== Garden Plant Registry ===")
    rose.show()
    sunflower.show()
    cactus.show()
