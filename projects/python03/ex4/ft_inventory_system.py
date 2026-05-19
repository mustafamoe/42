import sys


def parse_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    for argument in arguments:
        parts = argument.split(":")
        if len(parts) != 2:
            print(f"Error - invalid parameter '{argument}'")
            continue
        item_name = parts[0]
        if item_name in inventory.keys():
            print(f"Redundant item '{item_name}' - discarding")
            continue
        try:
            inventory[item_name] = int(parts[1])
        except ValueError as error:
            print(f"Quantity error for '{item_name}': {error}")
    return inventory


def get_extreme_item(
    inventory: dict[str, int],
    highest: bool,
) -> tuple[str, int]:
    item_name = ""
    quantity = 0
    first_item = True
    for current_name in inventory.keys():
        current_quantity = inventory[current_name]
        if first_item:
            item_name = current_name
            quantity = current_quantity
            first_item = False
        elif highest and current_quantity > quantity:
            item_name = current_name
            quantity = current_quantity
        elif not highest and current_quantity < quantity:
            item_name = current_name
            quantity = current_quantity
    return (item_name, quantity)


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")

    item_list = list(inventory.keys())
    total_quantity = sum(inventory.values())
    print(f"Item list: {item_list}")
    print(f"Total quantity of the {len(item_list)} items: {total_quantity}")

    if total_quantity != 0:
        for item_name in inventory.keys():
            quantity = inventory[item_name]
            percentage = round(quantity * 100 / total_quantity, 1)
            print(f"Item {item_name} represents {percentage}%")

        most_abundant = get_extreme_item(inventory, True)
        least_abundant = get_extreme_item(inventory, False)
        print(
            "Item most abundant: "
            f"{most_abundant[0]} with quantity {most_abundant[1]}"
        )
        print(
            "Item least abundant: "
            f"{least_abundant[0]} with quantity {least_abundant[1]}"
        )

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
