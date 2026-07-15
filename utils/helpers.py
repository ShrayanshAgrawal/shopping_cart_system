import os


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    print("\n" + "*" * 78)
    print(title.center(78))
    print("*" * 78)


def pause():
    input("\nPress Enter to continue...")


def get_int_input(prompt, min_value=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if min_value is not None and value < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")


def get_nonempty_input(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Input cannot be empty.")


def print_products(products):
    if not products:
        print("No products found.")
        return
    print("\n" + "-" * 78)
    print(f"{'ID':<6}{'Name':<25}{'Category':<14}{'Price':>10}{'Stock':>8}")
    print("-" * 78)
    for p in products:
        print(f"{p.product_id:<6}{p.name:<25}{p.category:<14}{p.price:>10.2f}{p.stock:>8}")
    print("-" * 78)