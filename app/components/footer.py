import reflex as rx


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Dream Knot",
                        class_name="text-2xl font-['Great_Vibes'] text-white",
                    ),
                    rx.el.p(
                        "Curated gifts for every occasion.",
                        class_name="text-gray-300 mt-2 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Shop",
                        class_name="font-bold font-['Playfair_Display'] text-white",
                    ),
                    rx.el.a(
                        "Birthday Gifts",
                        href="#",
                        class_name="mt-4 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "Anniversary",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "Corporate Gifts",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "Personalized",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "About",
                        class_name="font-bold font-['Playfair_Display'] text-white",
                    ),
                    rx.el.a(
                        "About Us",
                        href="#",
                        class_name="mt-4 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "Contact",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "FAQs",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Support",
                        class_name="font-bold font-['Playfair_Display'] text-white",
                    ),
                    rx.el.a(
                        "Shipping Info",
                        href="#",
                        class_name="mt-4 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                    rx.el.a(
                        "Return Policy",
                        href="#",
                        class_name="mt-2 block text-gray-300 hover:text-[#D4C08A]",
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Connect",
                        class_name="font-bold font-['Playfair_Display'] text-white",
                    ),
                    rx.el.div(
                        rx.el.a(rx.icon("instagram", class_name="h-6 w-6"), href="#"),
                        rx.el.a(rx.icon("facebook", class_name="h-6 w-6"), href="#"),
                        rx.el.a(rx.icon("twitter", class_name="h-6 w-6"), href="#"),
                        class_name="flex mt-4 space-x-4 text-gray-300 hover:[&>a]:text-[#D4C08A]",
                    ),
                ),
                class_name="grid grid-cols-2 md:grid-cols-5 gap-8 text-white",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2024 Dream Knot. All rights reserved.",
                    class_name="text-gray-400 text-sm",
                ),
                class_name="mt-12 pt-8 border-t border-white/20 text-center",
            ),
            class_name="container mx-auto px-4 py-12",
        ),
        class_name="bg-[#19325C]",
    )