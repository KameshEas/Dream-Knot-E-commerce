import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.states.cart_state import CartState, CartItem


def cart_item_row(item: CartItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=item["product"]["images"][0],
                class_name="w-24 h-24 object-cover rounded-lg",
            ),
            rx.el.div(
                rx.el.a(
                    item["product"]["name"],
                    href=f"/product/{item['product']['id']}",
                    class_name="font-bold text-lg text-[#19325C]",
                ),
                rx.el.p(
                    f"SKU: {item['product']['sku']}", class_name="text-sm text-gray-500"
                ),
                rx.el.button(
                    "Remove",
                    on_click=lambda: CartState.remove_from_cart(item["product"]["id"]),
                    class_name="text-red-500 text-sm hover:underline",
                ),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.p(
            f"₹{item['product']['price']:.2f}", class_name="font-bold text-[#19325C]"
        ),
        rx.el.div(
            rx.el.input(
                on_change=lambda val: CartState.update_quantity(
                    item["product"]["id"], val
                ),
                type="number",
                class_name="w-20 text-center border rounded-md py-1",
                default_value=item["quantity"].to_string(),
            )
        ),
        rx.el.p(
            f"₹{item['product']['price'] * item['quantity']:.2f}",
            class_name="font-bold text-[#19325C] text-right",
        ),
        class_name="grid grid-cols-[2fr,1fr,1fr,1fr] gap-4 items-center py-6 border-b",
    )


def cart_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Your Shopping Cart",
                    class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] mb-8",
                ),
                rx.cond(
                    CartState.item_count > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "Product",
                                        class_name="text-sm text-gray-500 uppercase",
                                    ),
                                    rx.el.h3(
                                        "Price",
                                        class_name="text-sm text-gray-500 uppercase",
                                    ),
                                    rx.el.h3(
                                        "Quantity",
                                        class_name="text-sm text-gray-500 uppercase",
                                    ),
                                    rx.el.h3(
                                        "Total",
                                        class_name="text-sm text-gray-500 uppercase text-right",
                                    ),
                                    class_name="grid grid-cols-[2fr,1fr,1fr,1fr] gap-4 pb-4 border-b",
                                ),
                                rx.foreach(CartState.cart_items, cart_item_row),
                                class_name="bg-white p-8 rounded-2xl shadow-sm border",
                            ),
                            rx.el.div(
                                rx.el.h2(
                                    "Order Summary",
                                    class_name="text-2xl font-bold text-[#19325C] mb-6",
                                ),
                                rx.el.div(
                                    rx.el.p("Subtotal"),
                                    rx.el.p(f"₹{CartState.subtotal:.2f}"),
                                    class_name="flex justify-between mb-2 text-lg",
                                ),
                                rx.el.div(
                                    rx.el.p("Shipping"),
                                    rx.el.p("Calculated at next step"),
                                    class_name="flex justify-between text-gray-600 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.p("Total", class_name="font-bold"),
                                    rx.el.p(
                                        f"₹{CartState.subtotal:.2f}",
                                        class_name="font-bold",
                                    ),
                                    class_name="flex justify-between text-xl border-t pt-4",
                                ),
                                rx.el.button(
                                    "Proceed to Checkout",
                                    on_click=CartState.proceed_to_checkout,
                                    class_name="mt-8 w-full bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-bold py-3 rounded-full hover:opacity-90 transition-opacity",
                                ),
                                class_name="bg-white p-8 rounded-2xl shadow-sm border h-fit",
                            ),
                            class_name="grid lg:grid-cols-[2fr,1fr] gap-8 items-start",
                        ),
                        rx.el.div(
                            rx.el.a(
                                "← Continue Shopping",
                                href="/products",
                                class_name="text-[#19325C] hover:underline font-bold",
                            ),
                            class_name="mt-8",
                        ),
                    ),
                    rx.el.div(
                        rx.icon(
                            tag="shopping-cart",
                            class_name="h-24 w-24 text-gray-300 mx-auto",
                        ),
                        rx.el.h2(
                            "Your cart is empty",
                            class_name="mt-6 text-2xl font-bold text-center text-gray-700",
                        ),
                        rx.el.p(
                            "Looks like you haven't added anything to your cart yet.",
                            class_name="mt-2 text-center text-gray-500",
                        ),
                        rx.el.a(
                            "Start Shopping",
                            href="/products",
                            class_name="mt-8 inline-block bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-['Playfair_Display'] font-bold py-3 px-8 rounded-full hover:opacity-90 transition-opacity",
                        ),
                        class_name="text-center bg-white p-16 rounded-2xl shadow-sm border",
                    ),
                ),
                class_name="container mx-auto px-4 py-12",
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )