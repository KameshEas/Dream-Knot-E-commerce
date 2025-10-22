import reflex as rx
from app.states.auth_state import AuthState
from app.states.cart_state import CartState
from app.states.product_state import ProductState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon(tag="gem", class_name="text-[#C1A86F] h-8 w-8"),
                    rx.el.span(
                        "Dream Knot",
                        class_name="text-3xl font-['Great_Vibes'] text-[#19325C]",
                    ),
                    class_name="flex items-center gap-2",
                ),
                href="/",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Search for gifts...",
                        class_name="w-full pl-10 pr-4 py-2 rounded-full border border-gray-300 focus:ring-2 focus:ring-[#D4C08A] focus:border-transparent transition font-['Playfair_Display']",
                    ),
                    rx.icon(
                        tag="search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    ),
                    class_name="relative w-full max-w-sm",
                )
            ),
            rx.el.nav(
                rx.foreach(
                    ProductState.categories,
                    lambda category: rx.el.a(
                        category,
                        href=f"/category/{category.lower()}",
                        class_name="text-[#19325C] hover:text-[#C1A86F] font-medium capitalize",
                    ),
                ),
                class_name="hidden md:flex items-center gap-6 font-['Playfair_Display']",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon(tag="shopping-cart", class_name="h-6 w-6"),
                        rx.cond(
                            CartState.item_count > 0,
                            rx.el.span(
                                CartState.item_count,
                                class_name="absolute -top-2 -right-2 bg-[#C1A86F] text-[#19325C] text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold",
                            ),
                            rx.fragment(),
                        ),
                        class_name="relative",
                    ),
                    href="/cart",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.cond(
                            AuthState.is_admin,
                            rx.el.a(
                                rx.icon(
                                    tag="shield-check",
                                    class_name="h-6 w-6 text-green-600",
                                ),
                                href="/admin",
                                title="Admin Dashboard",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.a(
                            rx.icon(tag="user", class_name="h-6 w-6"), href="/account"
                        ),
                        rx.el.button(
                            rx.icon(tag="log-out", class_name="h-5 w-5"),
                            on_click=AuthState.logout,
                            class_name="p-2 rounded-full hover:bg-gray-200 transition-colors",
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Login",
                            href="/login",
                            class_name="px-4 py-2 text-sm font-['Playfair_Display'] font-bold text-[#19325C] hover:text-[#C1A86F]",
                        ),
                        rx.el.a(
                            "Sign Up",
                            href="/signup",
                            class_name="px-4 py-2 text-sm font-['Playfair_Display'] font-bold text-[#19325C] bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] rounded-full hover:opacity-90 transition-colors",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex items-center gap-4 text-[#19325C]",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b border-gray-200",
    )