import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.states.auth_state import AuthState
from app.states.payment_state import PaymentState, Order


def account_sidebar() -> rx.Component:
    menu_items = [
        ("Profile", "/account", "user"),
        ("My Orders", "/account/orders", "package"),
        ("Wishlist", "/account/wishlist", "heart"),
        ("Addresses", "/account/addresses", "map-pin"),
    ]
    return rx.el.aside(
        rx.el.h3(
            "My Account",
            class_name="text-2xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.el.nav(
            rx.foreach(
                menu_items,
                lambda item: rx.el.a(
                    rx.icon(tag=item[2], class_name="h-5 w-5 mr-3"),
                    rx.el.span(item[0]),
                    href=item[1],
                    class_name="flex items-center px-4 py-3 rounded-lg text-[#19325C] hover:bg-[#F6E6B6]/50 transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon(tag="log-out", class_name="h-5 w-5 mr-3"),
                "Logout",
                on_click=AuthState.logout,
                class_name="w-full flex items-center px-4 py-3 mt-4 rounded-lg text-red-600 hover:bg-red-100 transition-colors",
            ),
            class_name="flex flex-col gap-2 font-medium",
        ),
        class_name="w-64 flex-shrink-0",
    )


def order_card(order: Order) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    f"Order #{order['id']}",
                    class_name="text-lg font-bold text-[#19325C]",
                ),
                rx.el.p(
                    f"Placed on {order['created_at'][:10]}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    order["status"].capitalize(),
                    class_name=rx.cond(
                        order["status"] == "confirmed",
                        "px-3 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full",
                        rx.cond(
                            order["status"] == "processing",
                            "px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full",
                            "px-3 py-1 bg-gray-100 text-gray-800 text-xs font-semibold rounded-full",
                        ),
                    ),
                ),
                class_name="text-right",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Total Amount:", class_name="font-semibold"),
                rx.el.p(
                    f"₹{order['total_amount']:.2f}",
                    class_name="font-bold text-[#19325C]",
                ),
                class_name="flex justify-between",
            ),
            rx.el.div(
                rx.el.p("Payment Method:", class_name="font-semibold"),
                rx.el.p(
                    rx.cond(
                        order["payment_method"]["type"] == "stripe",
                        "Credit/Debit Card",
                        "Cash on Delivery (COD)",
                    ),
                    class_name="capitalize",
                ),
                class_name="flex justify-between",
            ),
            rx.el.div(
                rx.el.p("Payment Status:", class_name="font-semibold"),
                rx.el.span(
                    order["payment_status"].capitalize(),
                    class_name=rx.cond(
                        order["payment_status"] == "paid",
                        "text-green-600 font-semibold",
                        rx.cond(
                            order["payment_status"] == "partial",
                            "text-yellow-600 font-semibold",
                            "text-red-600 font-semibold",
                        ),
                    ),
                ),
                class_name="flex justify-between",
            ),
            rx.cond(
                order["payment_method"]["type"] == "cod",
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Advance Paid:", class_name="text-sm text-gray-600"),
                        rx.el.p(
                            f"₹{order['cod_advance']:.2f}",
                            class_name="text-sm font-semibold text-green-600",
                        ),
                        class_name="flex justify-between",
                    ),
                    rx.el.div(
                        rx.el.p("On Delivery:", class_name="text-sm text-gray-600"),
                        rx.el.p(
                            f"₹{order['cod_remaining']:.2f}",
                            class_name="text-sm font-semibold text-[#C1A86F]",
                        ),
                        class_name="flex justify-between",
                    ),
                    class_name="mt-2 p-2 bg-[#F6E6B6]/30 rounded text-sm space-y-1",
                ),
                rx.fragment(),
            ),
            class_name="space-y-2 text-sm",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow",
    )


def account_page_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(account_sidebar(), content, class_name="flex-grow"),
                class_name="container mx-auto px-4 py-12 flex gap-12 items-start",
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )


def account_profile_content() -> rx.Component:
    return rx.el.main(
        rx.el.h2(
            "Profile",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.cond(
            AuthState.is_authenticated,
            rx.el.div(
                rx.el.div(
                    rx.el.label("Full Name", class_name="font-semibold text-gray-700"),
                    rx.el.input(
                        default_value=AuthState.logged_in_user["full_name"],
                        class_name="mt-1 w-full p-2 border rounded-md bg-gray-100",
                        disabled=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Email Address", class_name="font-semibold text-gray-700"
                    ),
                    rx.el.input(
                        default_value=AuthState.logged_in_user["email"],
                        type="email",
                        class_name="mt-1 w-full p-2 border rounded-md bg-gray-100",
                        disabled=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number", class_name="font-semibold text-gray-700"
                    ),
                    rx.el.input(
                        default_value=AuthState.logged_in_user["phone_number"],
                        class_name="mt-1 w-full p-2 border rounded-md bg-gray-100",
                        disabled=True,
                        placeholder="Not provided",
                    ),
                    class_name="mb-4",
                ),
                class_name="bg-white p-8 rounded-2xl shadow-sm border",
            ),
            rx.el.div(
                "Please log in to view your profile.",
                class_name="bg-white p-8 rounded-2xl shadow-sm border text-center text-gray-500",
            ),
        ),
    )


def orders_content() -> rx.Component:
    return rx.el.main(
        rx.el.h2(
            "My Orders",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.cond(
            PaymentState.orders.length() > 0,
            rx.el.div(
                rx.foreach(PaymentState.orders, order_card), class_name="space-y-6"
            ),
            rx.el.div(
                "You have not placed any orders yet.",
                class_name="bg-white p-8 rounded-2xl shadow-sm border text-center text-gray-500",
            ),
        ),
    )


def wishlist_content() -> rx.Component:
    return rx.el.main(
        rx.el.h2(
            "My Wishlist",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.el.div(
            "Your wishlist is empty.",
            class_name="bg-white p-8 rounded-2xl shadow-sm border text-center text-gray-500",
        ),
    )


def addresses_content() -> rx.Component:
    return rx.el.main(
        rx.el.h2(
            "My Addresses",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.el.div(
            "You have not saved any addresses yet.",
            class_name="bg-white p-8 rounded-2xl shadow-sm border text-center text-gray-500",
        ),
    )


def account_page() -> rx.Component:
    return account_page_layout(account_profile_content())


def orders_page() -> rx.Component:
    return account_page_layout(orders_content())


def wishlist_page() -> rx.Component:
    return account_page_layout(wishlist_content())


def addresses_page() -> rx.Component:
    return account_page_layout(addresses_content())