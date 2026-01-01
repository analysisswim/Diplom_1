class Burger:
    def __init__(self):
        self.bun = None
        self.ingredients = []

    def set_buns(self, bun):
        self.bun = bun

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def remove_ingredient(self, index: int):
        self.ingredients.pop(index)

    def move_ingredient(self, index: int, new_index: int):
        self.ingredients.insert(new_index, self.ingredients.pop(index))

    def get_price(self) -> float:
        bun_price = self.bun.get_price() if self.bun else 0
        ingredients_price = sum(ing.get_price() for ing in self.ingredients)
        return bun_price * 2 + ingredients_price

    def get_receipt(self) -> str:
        receipt = []
        receipt.append(f'(==== {self.bun.get_name()} ====)')
        for ingredient in self.ingredients:
            receipt.append(f'= {ingredient.get_type().lower()} {ingredient.get_name()} =')
        receipt.append(f'(==== {self.bun.get_name()} ====)\n')
        receipt.append(f'Price: {self.get_price()}')
        return '\n'.join(receipt)
