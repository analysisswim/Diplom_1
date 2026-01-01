import pytest
from unittest.mock import Mock

from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


def make_bun(name: str = "Space Bun", price: float = 100.0) -> Mock:
    bun = Mock(spec=Bun)
    bun.get_name.return_value = name
    bun.get_price.return_value = price
    return bun


def make_ingredient(typ: str, name: str, price: float) -> Mock:
    ing = Mock(spec=Ingredient)
    ing.get_type.return_value = typ
    ing.get_name.return_value = name
    ing.get_price.return_value = price
    return ing


def test_init_state(burger):
    assert burger.bun is None
    assert burger.ingredients == []


def test_set_buns_sets_bun(burger):
    bun = make_bun()
    burger.set_buns(bun)
    assert burger.bun is bun


def test_add_ingredient_appends_to_list(burger):
    burger.set_buns(make_bun())

    ing = make_ingredient(INGREDIENT_TYPE_SAUCE, "Ketchup", 10.0)
    burger.add_ingredient(ing)

    assert burger.ingredients == [ing]


@pytest.mark.parametrize(
    "remove_index, expected_order",
    [
        (0, ["B", "C"]),
        (1, ["A", "C"]),
        (2, ["A", "B"]),
    ],
)
def test_remove_ingredient_deletes_by_index(burger, remove_index, expected_order):
    burger.set_buns(make_bun())

    ings = [
        make_ingredient(INGREDIENT_TYPE_FILLING, "A", 1.0),
        make_ingredient(INGREDIENT_TYPE_FILLING, "B", 1.0),
        make_ingredient(INGREDIENT_TYPE_FILLING, "C", 1.0),
    ]
    for ing in ings:
        burger.add_ingredient(ing)

    burger.remove_ingredient(remove_index)

    assert [i.get_name() for i in burger.ingredients] == expected_order


@pytest.mark.parametrize(
    "index, new_index, expected_order",
    [
        (0, 2, ["B", "C", "A"]),
        (2, 0, ["C", "A", "B"]),
        (1, 1, ["A", "B", "C"]),
    ],
)
def test_move_ingredient_reorders_list(burger, index, new_index, expected_order):
    burger.set_buns(make_bun())

    ings = [
        make_ingredient(INGREDIENT_TYPE_FILLING, "A", 1.0),
        make_ingredient(INGREDIENT_TYPE_FILLING, "B", 1.0),
        make_ingredient(INGREDIENT_TYPE_FILLING, "C", 1.0),
    ]
    for ing in ings:
        burger.add_ingredient(ing)

    burger.move_ingredient(index, new_index)

    assert [i.get_name() for i in burger.ingredients] == expected_order


@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_total",
    [
        (50.0, [], 100.0),
        (80.0, [10.0], 170.0),
        (100.0, [10.0, 25.5], 235.5),
    ],
)
def test_get_price_calculates_bun_twice_plus_ingredients(burger, bun_price, ingredient_prices, expected_total):
    burger.set_buns(make_bun(price=bun_price))

    for i, p in enumerate(ingredient_prices):
        burger.add_ingredient(make_ingredient(INGREDIENT_TYPE_SAUCE, f"I{i}", p))

    assert burger.get_price() == expected_total


def test_get_receipt_formats_correctly(burger):
    bun_name = "Space Bun"
    burger.set_buns(make_bun(name=bun_name, price=100.0))

    ing1 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Sauce", 10.0)
    ing2 = make_ingredient(INGREDIENT_TYPE_FILLING, "Meat", 200.0)
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)

    receipt = burger.get_receipt()
    lines = receipt.split("\n")

    expected_price = 100.0 * 2 + 10.0 + 200.0

    # В burger.py последняя булка добавляется с "\n" в конце, поэтому тут есть пустая строка перед Price
    assert lines == [
        f"(==== {bun_name} ====)",
        "= sauce Sauce =",
        "= filling Meat =",
        f"(==== {bun_name} ====)",
        "",
        f"Price: {expected_price}",
    ]
