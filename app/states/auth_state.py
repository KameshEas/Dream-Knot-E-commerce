import reflex as rx
from typing import TypedDict


class User(TypedDict):
    full_name: str
    email: str
    password: str
    phone_number: str | None


class AuthState(rx.State):
    users: dict[str, User] = {
        "user@example.com": {
            "full_name": "John Doe",
            "email": "user@example.com",
            "password": "password123",
            "phone_number": "123-456-7890",
        }
    }
    logged_in_user: User | None = None
    show_login_toast: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_user is not None

    @rx.event
    def signup(self, form_data: dict):
        email = form_data["email"].lower()
        if email in self.users:
            return rx.toast.error("Email already exists.")
        if form_data["password"] != form_data["confirm_password"]:
            return rx.toast.error("Passwords do not match.")
        new_user: User = {
            "full_name": form_data["full_name"],
            "email": email,
            "password": form_data["password"],
            "phone_number": None,
        }
        self.users[email] = new_user
        self.logged_in_user = new_user
        return rx.redirect("/")

    @rx.event
    def login(self, form_data: dict):
        email = form_data["email"].lower()
        password = form_data["password"]
        user = self.users.get(email)
        if user and user["password"] == password:
            self.logged_in_user = user
            yield rx.toast.success("Login Successful!")
            return rx.redirect("/")
        else:
            return rx.toast.error("Invalid email or password.")

    @rx.event
    def logout(self):
        self.logged_in_user = None
        yield rx.toast.info("You have been logged out.")
        return rx.redirect("/")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")