import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.product_card import product_card
from app.states.product_state import ProductState


def category_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Category: ",
                    rx.el.span(
                        ProductState.current_category_name.capitalize(),
                        class_name="text-[#C1A86F]",
                    ),
                    class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] mb-12 text-center",
                ),
                rx.cond(
                    ProductState.products_in_category.length() > 0,
                    rx.el.div(
                        rx.foreach(ProductState.products_in_category, product_card),
                        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-x-8 gap-y-12",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "No products found in this category.",
                            class_name="text-center text-gray-500 italic",
                        ),
                        class_name="col-span-full",
                    ),
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )