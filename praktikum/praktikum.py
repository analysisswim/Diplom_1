from praktikum.database import Database
from praktikum.burger import Burger


def main():
    database = Database()
    burger = Burger()

    burger.set_buns(database.available_buns()[0])
    for ingredient in database.available_ingredients()[:3]:
        burger.add_ingredient(ingredient)

    print(burger.get_receipt())


if __name__ == "__main__":
    main()
