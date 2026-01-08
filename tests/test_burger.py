import pytest

from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE

from tests.data import (
    BUN_NAME,
    BUN_PRICE,
    SAUCE_NAME,
    SAUCE_PRICE,
)


@pytest.mark.unit
class TestBurger:
    def test_init_state(self, burger):
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns_sets_bun(self, burger, make_bun):
        bun = make_bun(name=BUN_NAME, price=BUN_PRICE)
        burger.set_buns(bun)
        assert burger.bun == bun

    def test_add_ingredient_appends_to_list(self, burger, make_bun, make_ingredient):
        burger.set_buns(make_bun(name=BUN_NAME, price=BUN_PRICE))

        ing = make_ingredient(INGREDIENT_TYPE_SAUCE, SAUCE_NAME, SAUCE_PRICE)
        burger.add_ingredient(ing)

        assert burger.ingredients == [ing]

    def test_remove_ingredient_removes_item(self, burger, make_bun, make_ingredient):
        burger.set_buns(make_bun(name=BUN_NAME, price=BUN_PRICE))

        ing1 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Ketchup", 10.0)
        ing2 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Mayo", 12.0)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.remove_ingredient(0)
        assert burger.ingredients == [ing2]

    def test_move_ingredient_moves_item(self, burger, make_bun, make_ingredient):
        burger.set_buns(make_bun(name=BUN_NAME, price=BUN_PRICE))

        ing1 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Ketchup", 10.0)
        ing2 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Mayo", 12.0)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.move_ingredient(1, 0)
        assert burger.ingredients == [ing2, ing1]

    def test_get_price_returns_total(self, burger, make_bun, make_ingredient):
        bun = make_bun(name=BUN_NAME, price=BUN_PRICE)
        burger.set_buns(bun)

        ing1 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Ketchup", 10.0)
        ing2 = make_ingredient(INGREDIENT_TYPE_SAUCE, "Mayo", 12.0)
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        # bun counted twice: top + bottom
        assert burger.get_price() == (BUN_PRICE * 2) + 10.0 + 12.0

    def test_get_receipt_contains_names_and_price(self, burger, make_bun, make_ingredient):
        bun = make_bun(name=BUN_NAME, price=BUN_PRICE)
        burger.set_buns(bun)

        ing = make_ingredient(INGREDIENT_TYPE_SAUCE, SAUCE_NAME, SAUCE_PRICE)
        burger.add_ingredient(ing)

        receipt = burger.get_receipt()
        assert BUN_NAME in receipt
        assert SAUCE_NAME in receipt
        assert str(burger.get_price()) in receipt
