import reflex as rx
import stripe
import os
from typing import TypedDict, Literal
from app.states.cart_state import CartState
from app.states.auth_state import AuthState
import logging


class PaymentMethod(TypedDict):
    type: Literal["stripe", "cod"]
    card_last4: str | None
    brand: str | None


class Order(TypedDict):
    id: str
    user_email: str
    items: list
    subtotal: float
    shipping_cost: float
    cod_advance: float | None
    cod_remaining: float | None
    total_amount: float
    payment_method: PaymentMethod
    shipping_address: dict
    status: Literal[
        "pending", "confirmed", "processing", "shipped", "delivered", "cancelled"
    ]
    payment_status: Literal["pending", "paid", "partial", "failed"]
    created_at: str
    stripe_payment_intent_id: str | None


class PaymentState(rx.State):
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    orders: list[Order] = []
    current_order: Order | None = None
    selected_payment_method: Literal["stripe", "cod"] = "stripe"
    processing_payment: bool = False
    payment_error: str = ""
    shipping_address: dict = {}
    shipping_cost: float = 50.0
    cod_advance_percentage: float = 50.0

    @rx.var
    def stripe_available(self) -> bool:
        return bool(self.stripe_publishable_key and os.getenv("STRIPE_SECRET_KEY"))

    @rx.var
    def cod_advance_amount(self) -> float:
        """Calculate 50% advance amount for COD"""
        from app.states.cart_state import CartState

        total = self.get_total_amount()
        return total * (self.cod_advance_percentage / 100)

    @rx.var
    def cod_remaining_amount(self) -> float:
        """Calculate remaining amount to be paid on delivery"""
        total = self.get_total_amount()
        return total - self.cod_advance_amount

    @rx.event
    def get_total_amount(self) -> float:
        """Get total amount including shipping"""
        return 1000.0 + self.shipping_cost

    @rx.event
    def set_payment_method(self, method: str):
        """Set the selected payment method"""
        self.selected_payment_method = method
        self.payment_error = ""

    @rx.event
    def update_shipping_address(self, form_data: dict):
        """Update shipping address from form"""
        self.shipping_address = {
            "full_name": form_data.get("full_name", ""),
            "email": form_data.get("email", ""),
            "address_line_1": form_data.get("address", ""),
            "city": form_data.get("city", ""),
            "state": form_data.get("state", ""),
            "postal_code": form_data.get("zip_code", ""),
            "phone": form_data.get("phone", ""),
        }

    @rx.event
    async def create_stripe_payment_intent(self):
        """Create Stripe Payment Intent"""
        if not self.stripe_available:
            self.payment_error = "Stripe is not properly configured"
            return
        try:
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            cart_state = await self.get_state(CartState)
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                self.payment_error = "Please log in to continue"
                return
            total_amount = cart_state.subtotal + self.shipping_cost
            amount_in_paise = int(total_amount * 100)
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency="inr",
                payment_method_types=["card"],
                description="Dream Knot - Gift Purchase",
                metadata={
                    "customer_email": auth_state.logged_in_user["email"],
                    "order_type": "full_payment",
                },
            )
            self.current_payment_intent_id = payment_intent.id
            self.client_secret = payment_intent.client_secret
            return payment_intent.client_secret
        except Exception as e:
            logging.exception(f"Error creating Stripe payment intent: {e}")
            self.payment_error = f"Payment setup failed: {str(e)}"
            return None

    @rx.event
    async def create_cod_advance_payment_intent(self):
        """Create Stripe Payment Intent for COD advance payment"""
        if not self.stripe_available:
            self.payment_error = "Stripe is not properly configured"
            return
        try:
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            cart_state = await self.get_state(CartState)
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                self.payment_error = "Please log in to continue"
                return
            advance_amount = self.cod_advance_amount
            amount_in_paise = int(advance_amount * 100)
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency="inr",
                payment_method_types=["card"],
                description="Dream Knot - COD Advance Payment (50%)",
                metadata={
                    "customer_email": auth_state.logged_in_user["email"],
                    "order_type": "cod_advance",
                    "advance_percentage": str(self.cod_advance_percentage),
                    "remaining_amount": str(self.cod_remaining_amount),
                },
            )
            self.current_payment_intent_id = payment_intent.id
            self.cod_client_secret = payment_intent.client_secret
            return payment_intent.client_secret
        except Exception as e:
            logging.exception(f"Error creating COD advance payment intent: {e}")
            self.payment_error = f"COD advance payment setup failed: {str(e)}"
            return None

    @rx.event
    async def process_payment(self):
        """Process the payment based on selected method"""
        self.processing_payment = True
        self.payment_error = ""
        try:
            cart_state = await self.get_state(CartState)
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                self.payment_error = "Please log in to continue"
                self.processing_payment = False
                return
            if not cart_state.cart_items:
                self.payment_error = "Your cart is empty"
                self.processing_payment = False
                return
            if self.selected_payment_method == "stripe":
                client_secret = await self.create_stripe_payment_intent()
                if client_secret:
                    yield PaymentState.create_order("stripe", "paid", None)
                    yield rx.toast.success("Payment processed successfully!")
                    yield rx.redirect("/account/orders")
                else:
                    yield rx.toast.error(self.payment_error or "Payment failed")
            elif self.selected_payment_method == "cod":
                client_secret = await self.create_cod_advance_payment_intent()
                if client_secret:
                    yield PaymentState.create_order(
                        "cod", "partial", self.cod_advance_amount
                    )
                    yield rx.toast.success(
                        f"COD order confirmed! Advance payment of ₹{self.cod_advance_amount:.2f} processed. Remaining ₹{self.cod_remaining_amount:.2f} to be paid on delivery."
                    )
                    yield rx.redirect("/account/orders")
                else:
                    yield rx.toast.error(
                        self.payment_error or "COD advance payment failed"
                    )
        except Exception as e:
            logging.exception(f"Error processing payment: {e}")
            self.payment_error = f"Payment processing failed: {str(e)}"
            yield rx.toast.error(self.payment_error)
        finally:
            self.processing_payment = False

    @rx.event
    async def create_order(
        self, payment_method: str, payment_status: str, advance_amount: float | None
    ):
        """Create a new order"""
        try:
            cart_state = await self.get_state(CartState)
            auth_state = await self.get_state(AuthState)
            import datetime
            import uuid

            order_id = f"DK{uuid.uuid4().hex[:8].upper()}"
            subtotal = cart_state.subtotal
            total_amount = subtotal + self.shipping_cost
            payment_method_info: PaymentMethod = {
                "type": payment_method,
                "card_last4": None,
                "brand": None,
            }
            new_order: Order = {
                "id": order_id,
                "user_email": auth_state.logged_in_user["email"],
                "items": cart_state.cart_items,
                "subtotal": subtotal,
                "shipping_cost": self.shipping_cost,
                "cod_advance": advance_amount,
                "cod_remaining": self.cod_remaining_amount
                if payment_method == "cod"
                else None,
                "total_amount": total_amount,
                "payment_method": payment_method_info,
                "shipping_address": self.shipping_address,
                "status": "confirmed",
                "payment_status": payment_status,
                "created_at": datetime.datetime.now().isoformat(),
                "stripe_payment_intent_id": getattr(
                    self, "current_payment_intent_id", None
                ),
            }
            self.orders.append(new_order)
            self.current_order = new_order
            cart_state.items = {}
        except Exception as e:
            logging.exception(f"Error creating order: {e}")
            raise