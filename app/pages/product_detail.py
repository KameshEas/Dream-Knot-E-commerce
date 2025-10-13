import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.states.product_state import ProductState
from app.states.cart_state import CartState


def product_detail_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.cond(
                ProductState.selected_product,
                rx.el.div(
                    rx.el.div(
                        rx.el.img(
                            src=ProductState.selected_product["images"][0],
                            class_name="w-full aspect-square object-cover rounded-2xl shadow-lg",
                        )
                    ),
                    rx.el.div(
                        rx.el.h1(
                            ProductState.selected_product["name"],
                            class_name="text-4xl font-black font-['Playfair_Display'] text-[#19325C]",
                        ),
                        rx.el.p(
                            f"SKU: {ProductState.selected_product['sku']}",
                            class_name="text-sm text-gray-500 mt-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "star",
                                class_name="h-5 w-5 text-[#D4C08A] fill-[#D4C08A]",
                            ),
                            rx.el.span(
                                f"{ProductState.selected_product['rating']} ({ProductState.selected_product['num_reviews']} reviews)",
                                class_name="text-sm text-gray-600 ml-2",
                            ),
                            class_name="flex items-center my-4",
                        ),
                        rx.el.p(
                            ProductState.selected_product["description"],
                            class_name="text-gray-700 leading-relaxed",
                        ),
                        rx.el.div(
                            rx.el.p(
                                f"₹{ProductState.selected_product['price']:.2f}",
                                class_name="text-3xl font-bold text-[#19325C]",
                            ),
                            rx.cond(
                                ProductState.selected_product["original_price"] != None,
                                rx.el.p(
                                    f"₹{ProductState.selected_product['original_price']:.2f}",
                                    class_name="text-xl text-gray-400 line-through",
                                ),
                                rx.fragment(),
                            ),
                            class_name="flex items-baseline gap-3 my-6",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Quantity", class_name="font-bold"),
                                rx.el.input(
                                    default_value="1",
                                    type="number",
                                    min=1,
                                    class_name="w-20 text-center border rounded-md py-2 px-3 mt-1",
                                ),
                                class_name="flex flex-col",
                            ),
                            rx.el.button(
                                rx.icon("shopping-cart", class_name="mr-2"),
                                "Add to Cart",
                                on_click=lambda: CartState.add_to_cart(
                                    ProductState.selected_product["id"]
                                ),
                                class_name="w-full bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-bold py-3 rounded-full hover:opacity-90 transition-opacity",
                            ),
                            class_name="flex items-end gap-4 mt-8",
                        ),
                    ),
                    class_name="container mx-auto px-4 py-12 grid md:grid-cols-2 gap-12 items-start",
                ),
                rx.el.div(
                    "Loading product...",
                    class_name="container mx-auto px-4 py-12 text-center text-gray-500",
                ),
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )