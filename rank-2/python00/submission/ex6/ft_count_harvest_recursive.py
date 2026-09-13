def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def print_day(day):
        if day > days:
            return
        print(f"Day {day}")
        print_day(day + 1)

    print_day(1)
    print("Harvest time!")
