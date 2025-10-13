import reflex as rx
from app.states.product_state import Product
from app.states.cart_state import CartState


def product_card(product: Product) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.el.img(
                    src=product["images"][0],
                    alt=product["name"],
                    class_name="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300",
                ),
                href=f"/product/{product['id']}",
            ),
            rx.cond(
                product["original_price"] != None,
                rx.el.span(
                    "Sale",
                    class_name="absolute top-3 left-3 bg-[#19325C] text-white text-xs font-bold px-2 py-1 rounded-full",
                ),
                rx.fragment(),
            ),
            class_name="relative w-full aspect-square overflow-hidden rounded-lg bg-gray-100 group",
        ),
        rx.el.div(
            rx.el.h3(
                rx.el.a(
                    product["name"],
                    href=f"/product/{product['id']}",
                    class_name="hover:text-[#C1A86F]",
                ),
                class_name="text-base font-['Playfair_Display'] font-bold text-[#19325C] truncate",
            ),
            rx.el.div(
                rx.el.p(
                    f"₹{product['price']:.2f}",
                    class_name="text-lg font-['Playfair_Display'] font-bold text-[#19325C]",
                ),
                rx.cond(
                    product["original_price"] != None,
                    rx.el.p(
                        f"₹{product['original_price']:.2f}",
                        class_name="text-sm text-gray-500 line-through",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-baseline gap-2",
            ),
            rx.el.div(
                rx.icon("star", class_name="h-4 w-4 text-[#D4C08A] fill-[#D4C08A]"),
                rx.el.span(
                    f"{product['rating']} ({product['num_reviews']})",
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="mt-4 flex flex-col gap-2",
        ),
        rx.el.button(
            rx.icon("shopping-cart", class_name="h-5 w-5 mr-2"),
            "Add to Cart",
            on_click=lambda: CartState.add_to_cart(product["id"]),
            class_name="mt-4 w-full flex items-center justify-center px-4 py-2 bg-white border-2 border-[#19325C] text-[#19325C] font-['Playfair_Display'] font-bold rounded-full hover:bg-[#19325C] hover:text-white transition-colors",
        ),
        class_name="flex flex-col",
    )