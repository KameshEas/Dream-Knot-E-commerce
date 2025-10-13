import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.product_card import product_card
from app.states.product_state import ProductState


def products_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "All Gifts",
                    class_name="text-5xl font-['Playfair_Display'] font-black text-[#19325C] mb-4 text-center",
                ),
                rx.el.p(
                    "Discover the perfect present for any occasion from our curated collection.",
                    class_name="text-lg text-gray-600 text-center max-w-2xl mx-auto",
                ),
                class_name="py-16 bg-white",
            ),
            rx.el.div(
                rx.el.aside(
                    rx.el.h3(
                        "Filters",
                        class_name="text-xl font-bold text-[#19325C] mb-6 border-b pb-3",
                    ),
                    rx.el.div(
                        rx.el.h4("Category", class_name="font-semibold mb-3"),
                        rx.foreach(
                            ProductState.categories,
                            lambda category: rx.el.a(
                                category,
                                href=f"/category/{category.lower()}",
                                class_name="block py-1 hover:text-[#C1A86F]",
                            ),
                        ),
                        class_name="mb-8",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            f"Showing {ProductState.products.length()} products",
                            class_name="text-sm text-gray-600",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.cond(
                        ProductState.products.length() > 0,
                        rx.el.div(
                            rx.foreach(ProductState.products, product_card),
                            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12",
                        ),
                        rx.el.p("No products found."),
                    ),
                ),
                class_name="container mx-auto px-4 py-12 grid lg:grid-cols-[280px,1fr] gap-12 items-start",
            ),
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )