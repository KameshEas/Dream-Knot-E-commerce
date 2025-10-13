import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.product_card import product_card
from app.states.product_state import ProductState
from app.pages.login import login_page
from app.pages.signup import signup_page
from app.pages.products import products_page
from app.pages.product_detail import product_detail_page
from app.pages.category import category_page
from app.pages.cart import cart_page
from app.pages.checkout import checkout_page
from app.pages.account import account_page, orders_page, wishlist_page, addresses_page
from app.pages.admin import admin_page, admin_products_page
from app.states.auth_state import AuthState


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.img(
                src="placeholder.svg",
                class_name="absolute inset-0 w-full h-full object-cover",
            ),
            rx.el.div(class_name="absolute inset-0 bg-[#19325C]/70"),
            rx.el.div(
                rx.el.h1(
                    "Find the Perfect Gift",
                    class_name="text-5xl md:text-7xl text-white font-['Great_Vibes']",
                ),
                rx.el.p(
                    "Curated gift collections for every special occasion.",
                    class_name="mt-4 max-w-xl text-lg text-white font-['Playfair_Display'] italic",
                ),
                rx.el.a(
                    "Shop Now",
                    href="/products",
                    class_name="mt-8 inline-block bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-['Playfair_Display'] font-bold py-3 px-8 rounded-full hover:opacity-90 transition-opacity",
                ),
                class_name="relative z-10 text-center px-4",
            ),
            class_name="relative flex items-center justify-center h-[60vh] bg-gray-800 text-white overflow-hidden",
        )
    )


def categories_section() -> rx.Component:
    categories = [
        ("Birthday", "gift"),
        ("Anniversary", "heart"),
        ("Corporate", "briefcase"),
        ("Personalized", "edit-3"),
    ]
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Shop by Category",
                class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] text-center",
            ),
            rx.el.div(
                rx.foreach(
                    categories,
                    lambda cat: rx.el.a(
                        rx.el.div(
                            rx.icon(tag=cat[1], class_name="h-10 w-10 text-[#C1A86F]"),
                            rx.el.h3(
                                cat[0],
                                class_name="mt-4 text-lg font-['Playfair_Display'] font-bold text-[#19325C]",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 bg-white rounded-2xl shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-300 border border-gray-200",
                        ),
                        href=f"/category/{cat[0].lower().replace(' ', '-')}",
                    ),
                ),
                class_name="mt-12 grid grid-cols-2 md:grid-cols-4 gap-8",
            ),
            class_name="container mx-auto px-4 py-20",
        ),
        class_name="bg-[#FCFAF5]",
    )


def featured_products_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Featured Products",
                class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] text-center",
            ),
            rx.el.div(
                rx.foreach(ProductState.featured_products, product_card),
                class_name="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-12",
            ),
            class_name="container mx-auto px-4 py-20",
        ),
        class_name="bg-white",
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(hero_section(), categories_section(), featured_products_section()),
        footer(),
        class_name="bg-white font-['Playfair_Display']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")
app.add_page(products_page, route="/products")
app.add_page(
    product_detail_page,
    route="/product/[product_id]",
    on_load=ProductState.get_product_details,
)
app.add_page(category_page, route="/category/[category_name]")
app.add_page(cart_page, route="/cart")
app.add_page(checkout_page, route="/checkout", on_load=AuthState.check_login)
app.add_page(account_page, route="/account", on_load=AuthState.check_login)
app.add_page(orders_page, route="/account/orders", on_load=AuthState.check_login)
app.add_page(wishlist_page, route="/account/wishlist", on_load=AuthState.check_login)
app.add_page(addresses_page, route="/account/addresses", on_load=AuthState.check_login)
app.add_page(admin_page, route="/admin", on_load=AuthState.check_admin)
app.add_page(
    admin_products_page, route="/admin/products", on_load=AuthState.check_admin
)