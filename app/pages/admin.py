import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.states.auth_state import AuthState
from app.states.product_state import ProductState, Product
from app.components.product_card import product_card


def admin_sidebar() -> rx.Component:
    menu_items = [
        ("Dashboard", "/admin", "layout-dashboard"),
        ("Products", "/admin/products", "package"),
        ("Orders", "/account/orders", "shopping-cart"),
        ("Go to Site", "/", "arrow-left-right"),
    ]
    return rx.el.aside(
        rx.el.h3(
            "Admin Panel",
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


def admin_page_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(admin_sidebar(), content, class_name="flex-grow"),
                class_name="container mx-auto px-4 py-12 flex gap-12 items-start",
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )


def create_product_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Create New Product", class_name="text-2xl font-bold text-[#19325C] mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label("Product Name", class_name="font-semibold"),
                    rx.el.input(
                        name="name",
                        required=True,
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.label("SKU", class_name="font-semibold"),
                    rx.el.input(
                        name="sku",
                        required=True,
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                class_name="grid md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Price", class_name="font-semibold"),
                    rx.el.input(
                        name="price",
                        type="number",
                        step="0.01",
                        required=True,
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.label(
                        "Original Price (Optional)", class_name="font-semibold"
                    ),
                    rx.el.input(
                        name="original_price",
                        type="number",
                        step="0.01",
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                class_name="grid md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.label("Description", class_name="font-semibold"),
                rx.el.textarea(
                    name="description",
                    required=True,
                    class_name="mt-1 w-full p-2 border rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Category", class_name="font-semibold"),
                    rx.el.input(
                        name="category",
                        required=True,
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.el.label("Stock", class_name="font-semibold"),
                    rx.el.input(
                        name="stock",
                        type="number",
                        required=True,
                        class_name="mt-1 w-full p-2 border rounded-md",
                    ),
                    class_name="w-full",
                ),
                class_name="grid md:grid-cols-2 gap-4 mb-4",
            ),
            rx.el.button(
                "Create Product",
                type="submit",
                class_name="px-6 py-2 bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] text-[#19325C] font-bold rounded-full hover:opacity-90",
            ),
            on_submit=ProductState.create_product,
            reset_on_submit=True,
        ),
        class_name="p-8 bg-white rounded-2xl shadow-sm border",
    )


def best_selling_products_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Best Selling Products", class_name="text-2xl font-bold text-[#19325C] mb-4"
        ),
        rx.cond(
            ProductState.best_selling_products.length() > 0,
            rx.el.div(
                rx.foreach(ProductState.best_selling_products, product_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
            ),
            rx.el.p("No products to display."),
        ),
        class_name="mt-12",
    )


def admin_dashboard_content() -> rx.Component:
    return rx.el.main(
        rx.el.h1(
            "Dashboard",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        rx.el.div(
            rx.el.p(
                f"Welcome back, {AuthState.logged_in_user['full_name']}!",
                class_name="text-lg",
            ),
            class_name="p-8 bg-white rounded-2xl shadow-sm border mb-8",
        ),
        best_selling_products_section(),
    )


def admin_products_content() -> rx.Component:
    return rx.el.main(
        rx.el.h1(
            "Product Management",
            class_name="text-3xl font-bold font-['Playfair_Display'] text-[#19325C] mb-6",
        ),
        create_product_form(),
    )


def admin_page() -> rx.Component:
    return admin_page_layout(admin_dashboard_content())


def admin_products_page() -> rx.Component:
    return admin_page_layout(admin_products_content())