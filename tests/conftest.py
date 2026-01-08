import pytest
from unittest.mock import Mock

from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient

@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def make_bun():
    """Factory fixture to build a Bun mock with custom name/price."""

    def _make_bun(name: str = "Space Bun", price: float = 100.0) -> Mock:
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name
        bun.get_price.return_value = price
        return bun

    return _make_bun


@pytest.fixture
def make_ingredient():
    """Factory fixture to build an Ingredient mock with custom type/name/price."""

    def _make_ingredient(typ: str, name: str, price: float) -> Mock:
        ing = Mock(spec=Ingredient)
        ing.get_type.return_value = typ
        ing.get_name.return_value = name
        ing.get_price.return_value = price
        return ing

    return _make_ingredient
