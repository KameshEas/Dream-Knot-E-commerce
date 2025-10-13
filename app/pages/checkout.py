import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.states.cart_state import CartState, CartItem
from app.states.auth_state import AuthState
from app.states.payment_state import PaymentState


def order_summary_item(item: CartItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=item["product"]["images"][0],
                class_name="w-16 h-16 object-cover rounded-md",
            ),
            rx.el.div(
                rx.el.p(item["product"]["name"], class_name="font-semibold"),
                rx.el.p(f"Qty: {item['quantity']}", class_name="text-sm text-gray-500"),
                class_name="ml-4",
            ),
            class_name="flex items-center",
        ),
        rx.el.p(
            f"₹{item['product']['price'] * item['quantity']:.2f}",
            class_name="font-semibold",
        ),
        class_name="flex justify-between items-center",
    )


def payment_method_selection() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Payment Method",
            class_name="text-lg font-bold font-['Playfair_Display'] text-[#19325C] mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    type="radio",
                    name="payment_method",
                    value="stripe",
                    checked=PaymentState.selected_payment_method == "stripe",
                    on_change=lambda: PaymentState.set_payment_method("stripe"),
                    class_name="mr-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("credit-card", class_name="h-5 w-5 text-[#C1A86F]"),
                        rx.el.span("Credit/Debit Card", class_name="font-semibold"),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p(
                        "Pay the full amount securely with Stripe",
                        class_name="text-sm text-gray-600 mt-1",
                    ),
                    rx.cond(
                        ~PaymentState.stripe_available,
                        rx.el.p(
                            "⚠️ Stripe not configured. Please add API keys.",
                            class_name="text-xs text-red-500 mt-1",
                        ),
                        rx.fragment(),
                    ),
                ),
                class_name="flex items-start p-4 border rounded-lg hover:bg-gray-50 cursor-pointer",
                on_click=lambda: PaymentState.set_payment_method("stripe"),
            ),
            rx.el.div(
                rx.el.input(
                    type="radio",
                    name="payment_method",
                    value="cod",
                    checked=PaymentState.selected_payment_method == "cod",
                    on_change=lambda: PaymentState.set_payment_method("cod"),
                    class_name="mr-3",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("banknote", class_name="h-5 w-5 text-[#C1A86F]"),
                        rx.el.span(
                            "Cash on Delivery (COD)", class_name="font-semibold"
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p(
                        f"Pay 50% advance (₹{PaymentState.cod_advance_amount:.2f}) now, remaining ₹{PaymentState.cod_remaining_amount:.2f} on delivery",
                        class_name="text-sm text-gray-600 mt-1",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span("Advance Payment:", class_name="font-medium"),
                            rx.el.span(
                                f"₹{PaymentState.cod_advance_amount:.2f}",
                                class_name="text-[#19325C] font-bold",
                            ),
                            class_name="flex justify-between",
                        ),
                        rx.el.div(
                            rx.el.span("On Delivery:", class_name="font-medium"),
                            rx.el.span(
                                f"₹{PaymentState.cod_remaining_amount:.2f}",
                                class_name="text-[#C1A86F] font-bold",
                            ),
                            class_name="flex justify-between",
                        ),
                        class_name="mt-2 p-2 bg-[#F6E6B6]/30 rounded text-xs space-y-1",
                    ),
                ),
                class_name="flex items-start p-4 border rounded-lg hover:bg-gray-50 cursor-pointer",
                on_click=lambda: PaymentState.set_payment_method("cod"),
            ),
            class_name="space-y-4",
        ),
        class_name="mb-8",
    )


def order_summary_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Order Summary",
            class_name="text-2xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.el.div(
            rx.foreach(CartState.cart_items, order_summary_item),
            class_name="space-y-4 border-b border-t py-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Subtotal"),
                rx.el.p(f"₹{CartState.subtotal:.2f}"),
                class_name="flex justify-between mt-4",
            ),
            rx.el.div(
                rx.el.p("Shipping"),
                rx.el.p(f"₹{PaymentState.shipping_cost:.2f}"),
                class_name="flex justify-between text-gray-600",
            ),
            rx.cond(
                PaymentState.selected_payment_method == "cod",
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Total Amount", class_name="font-semibold"),
                        rx.el.p(
                            f"₹{CartState.subtotal + PaymentState.shipping_cost:.2f}",
                            class_name="font-semibold",
                        ),
                        class_name="flex justify-between text-gray-600 border-t pt-2 mt-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Advance Payment (50%)",
                            class_name="font-bold text-[#19325C]",
                        ),
                        rx.el.p(
                            f"₹{PaymentState.cod_advance_amount:.2f}",
                            class_name="font-bold text-[#19325C]",
                        ),
                        class_name="flex justify-between bg-[#F6E6B6]/50 p-2 rounded mt-2",
                    ),
                    rx.el.div(
                        rx.el.p("On Delivery", class_name="text-[#C1A86F] font-medium"),
                        rx.el.p(
                            f"₹{PaymentState.cod_remaining_amount:.2f}",
                            class_name="text-[#C1A86F] font-bold",
                        ),
                        class_name="flex justify-between mt-2",
                    ),
                ),
                rx.fragment(),
            ),
            class_name="space-y-2 py-4 border-b",
        ),
        rx.cond(
            PaymentState.selected_payment_method == "stripe",
            rx.el.div(
                rx.el.p("Total to Pay", class_name="font-bold text-lg"),
                rx.el.p(
                    f"₹{CartState.subtotal + PaymentState.shipping_cost:.2f}",
                    class_name="font-bold text-lg",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Advance to Pay Now", class_name="font-bold text-lg text-[#19325C]"
                ),
                rx.el.p(
                    f"₹{PaymentState.cod_advance_amount:.2f}",
                    class_name="font-bold text-lg text-[#19325C]",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
        ),
        rx.cond(
            PaymentState.payment_error != "",
            rx.el.div(
                rx.el.p(PaymentState.payment_error, class_name="text-red-600 text-sm"),
                class_name="mt-4 p-3 bg-red-100 border border-red-300 rounded",
            ),
            rx.fragment(),
        ),
        class_name="w-full lg:w-2/5 lg:sticky top-28 h-fit bg-white p-8 rounded-2xl shadow-sm border",
    )


def checkout_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Checkout",
                    class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] mb-8 text-center",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Shipping Information",
                            class_name="text-2xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label("Full Name", class_name="font-semibold"),
                                rx.el.input(
                                    name="full_name",
                                    default_value=AuthState.logged_in_user["full_name"],
                                    class_name="mt-1 w-full p-2 border rounded-md",
                                    required=True,
                                ),
                                rx.el.label(
                                    "Email Address", class_name="font-semibold mt-4"
                                ),
                                rx.el.input(
                                    name="email",
                                    default_value=AuthState.logged_in_user["email"],
                                    type="email",
                                    class_name="mt-1 w-full p-2 border rounded-md",
                                    required=True,
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                            ),
                            rx.el.label(
                                "Phone Number", class_name="font-semibold mt-4"
                            ),
                            rx.el.input(
                                name="phone",
                                placeholder="Your phone number",
                                type="tel",
                                class_name="mt-1 w-full p-2 border rounded-md",
                                required=True,
                            ),
                            rx.el.label("Address", class_name="font-semibold mt-4"),
                            rx.el.input(
                                name="address",
                                placeholder="Street address",
                                class_name="mt-1 w-full p-2 border rounded-md",
                                required=True,
                            ),
                            rx.el.div(
                                rx.el.input(
                                    name="city",
                                    placeholder="City",
                                    class_name="mt-2 w-full p-2 border rounded-md",
                                    required=True,
                                ),
                                rx.el.input(
                                    name="state",
                                    placeholder="State",
                                    class_name="mt-2 w-full p-2 border rounded-md",
                                    required=True,
                                ),
                                rx.el.input(
                                    name="zip_code",
                                    placeholder="ZIP Code",
                                    class_name="mt-2 w-full p-2 border rounded-md",
                                    required=True,
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2",
                            ),
                            on_submit=PaymentState.update_shipping_address,
                            class_name="mb-8",
                        ),
                        payment_method_selection(),
                        rx.el.button(
                            rx.cond(
                                PaymentState.processing_payment,
                                rx.el.div(
                                    rx.spinner(size="2"),
                                    "Processing...",
                                    class_name="flex items-center gap-2",
                                ),
                                rx.cond(
                                    PaymentState.selected_payment_method == "stripe",
                                    "Pay Full Amount",
                                    "Pay Advance & Confirm COD",
                                ),
                            ),
                            on_click=PaymentState.process_payment,
                            disabled=PaymentState.processing_payment,
                            class_name="mt-8 w-full bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-bold py-3 rounded-full hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed",
                        ),
                        class_name="w-full",
                    ),
                    order_summary_sidebar(),
                    class_name="container mx-auto px-4 py-12 flex flex-col-reverse lg:flex-row gap-12 items-start",
                ),
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )