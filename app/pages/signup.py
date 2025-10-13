import reflex as rx
from app.states.auth_state import AuthState
from app.components.navbar import navbar
from app.components.footer import footer


def signup_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Create an Account",
                        class_name="text-4xl font-['Playfair_Display'] font-black text-[#19325C] mb-2 text-center",
                    ),
                    rx.el.p(
                        "Join Dream Knot to find the perfect gift.",
                        class_name="text-gray-500 mb-8 text-center italic",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Full Name",
                                html_for="full_name",
                                class_name="text-sm font-bold text-[#19325C]",
                            ),
                            rx.el.input(
                                type="text",
                                id="full_name",
                                name="full_name",
                                placeholder="John Doe",
                                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#D4C08A] focus:border-[#D4C08A]",
                                required=True,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email Address",
                                html_for="email",
                                class_name="text-sm font-bold text-[#19325C]",
                            ),
                            rx.el.input(
                                type="email",
                                id="email",
                                name="email",
                                placeholder="you@example.com",
                                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#D4C08A] focus:border-[#D4C08A]",
                                required=True,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                html_for="password",
                                class_name="text-sm font-bold text-[#19325C]",
                            ),
                            rx.el.input(
                                type="password",
                                id="password",
                                name="password",
                                placeholder="Minimum 8 characters",
                                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#D4C08A] focus:border-[#D4C08A]",
                                required=True,
                                min_length=8,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Confirm Password",
                                html_for="confirm_password",
                                class_name="text-sm font-bold text-[#19325C]",
                            ),
                            rx.el.input(
                                type="password",
                                id="confirm_password",
                                name="confirm_password",
                                placeholder="Re-enter your password",
                                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#D4C08A] focus:border-[#D4C08A]",
                                required=True,
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.button(
                            "Create Account",
                            type="submit",
                            class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-full shadow-sm text-sm font-bold text-[#19325C] bg-gradient-to-r from-[#F6E6B6] to-[#C1A86F] hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#C1A86F]",
                        ),
                        on_submit=AuthState.signup,
                        reset_on_submit=True,
                    ),
                    rx.el.p(
                        "Already have an account? ",
                        rx.el.a(
                            "Log in",
                            href="/login",
                            class_name="font-bold text-[#19325C] hover:text-[#C1A86F]",
                        ),
                        class_name="mt-6 text-center text-sm text-gray-600",
                    ),
                    class_name="max-w-md w-full bg-white p-10 rounded-2xl shadow-lg border border-gray-200",
                ),
                class_name="min-h-[calc(100vh-200px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8",
            )
        ),
        footer(),
        class_name="bg-[#FCFAF5] font-['Playfair_Display']",
    )