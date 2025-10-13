import reflex as rx
from typing import TypedDict
from app.states.product_state import Product


class CartItem(TypedDict):
    product: Product
    quantity: int


class CartState(rx.State):
    items: dict[int, CartItem] = {}

    @rx.var
    def cart_items(self) -> list[CartItem]:
        return list(self.items.values())

    @rx.var
    def item_count(self) -> int:
        return sum((item["quantity"] for item in self.items.values()))

    @rx.var
    def subtotal(self) -> float:
        return sum(
            (
                item["product"]["price"] * item["quantity"]
                for item in self.items.values()
            )
        )

    @rx.event
    async def add_to_cart(self, product_id: int, quantity: int = 1):
        if product_id in self.items:
            self.items[product_id]["quantity"] += quantity
        else:
            from app.states.product_state import ProductState

            product_state = await self.get_state(ProductState)
            product = next(
                (p for p in product_state.products if p["id"] == product_id), None
            )
            if product:
                self.items[product_id] = {"product": product, "quantity": quantity}
        yield rx.toast.success(f"Added to cart!")

    @rx.event
    def remove_from_cart(self, product_id: int):
        if product_id in self.items:
            del self.items[product_id]

    @rx.event
    def update_quantity(self, product_id: int, quantity: int):
        if product_id in self.items:
            if int(quantity) > 0:
                self.items[product_id]["quantity"] = int(quantity)
            else:
                del self.items[product_id]

    @rx.event
    async def proceed_to_checkout(self):
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.info("Please log in to proceed to checkout.")
            yield rx.redirect("/login")
            return
        yield rx.redirect("/checkout")
        return