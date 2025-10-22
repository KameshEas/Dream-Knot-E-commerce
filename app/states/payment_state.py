import reflex as rx
import stripe
import os
from typing import TypedDict, Literal
from app.states.cart_state import CartState
from app.states.auth_state import AuthState
from app.states.product_state import (
    ProductState,
    STRAPI_URL,
    STRAPI_API_TOKEN,
    STRAPI_CONFIGURED,
)
import logging
import requests
import json


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
    async def total_amount_computed(self) -> float:
        """Computes total amount from cart subtotal and shipping."""
        cart_state = await self.get_state(CartState)
        return cart_state.subtotal + self.shipping_cost

    @rx.var
    async def cod_advance_amount(self) -> float:
        """Calculate 50% advance amount for COD"""
        return await self.total_amount_computed * (self.cod_advance_percentage / 100)

    @rx.var
    async def cod_remaining_amount(self) -> float:
        """Calculate remaining amount to be paid on delivery"""
        return await self.total_amount_computed - await self.cod_advance_amount

    @rx.event
    def set_payment_method(self, method: str):
        self.selected_payment_method = method
        self.payment_error = ""

    @rx.event
    def update_shipping_address(self, form_data: dict):
        self.shipping_address = {
            "full_name": form_data.get("full_name", ""),
            "email": form_data.get("email", ""),
            "address_line_1": form_data.get("address", ""),
            "city": form_data.get("city", ""),
            "state": form_data.get("state", ""),
            "postal_code": form_data.get("zip_code", ""),
            "phone": form_data.get("phone", ""),
        }

    async def _create_stripe_payment_intent_base(
        self, amount: float, description: str, metadata: dict
    ):
        if not self.stripe_available:
            self.payment_error = "Stripe is not properly configured"
            return None
        try:
            stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
            amount_in_paise = int(amount * 100)
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency="inr",
                payment_method_types=["card"],
                description=description,
                metadata=metadata,
            )
            return payment_intent
        except Exception as e:
            logging.exception(f"Error creating Stripe payment intent: {e}")
            self.payment_error = f"Payment setup failed: {str(e)}"
            return None

    @rx.event
    async def create_stripe_payment_intent(self) -> str | None:
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            self.payment_error = "Please log in to continue"
            return None
        total_amount = await self.total_amount_computed
        metadata = {
            "customer_email": auth_state.logged_in_user["email"],
            "order_type": "full_payment",
        }
        payment_intent = await self._create_stripe_payment_intent_base(
            total_amount, "Dream Knot - Gift Purchase", metadata
        )
        if payment_intent:
            self.current_payment_intent_id = payment_intent.id
            return payment_intent.client_secret
        return None

    @rx.event
    async def create_cod_advance_payment_intent(self) -> str | None:
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            self.payment_error = "Please log in to continue"
            return None
        advance_amount = await self.cod_advance_amount
        metadata = {
            "customer_email": auth_state.logged_in_user["email"],
            "order_type": "cod_advance",
            "remaining_amount": str(await self.cod_remaining_amount),
        }
        payment_intent = await self._create_stripe_payment_intent_base(
            advance_amount, "Dream Knot - COD Advance (50%)", metadata
        )
        if payment_intent:
            self.current_payment_intent_id = payment_intent.id
            return payment_intent.client_secret
        return None

    @rx.event
    async def process_payment(self):
        self.processing_payment = True
        self.payment_error = ""
        try:
            auth_state = await self.get_state(AuthState)
            if not auth_state.is_authenticated:
                self.payment_error = "Please log in to continue"
                return
            cart_state = await self.get_state(CartState)
            if not cart_state.cart_items:
                self.payment_error = "Your cart is empty"
                return
            if self.selected_payment_method == "stripe":
                client_secret = await self.create_stripe_payment_intent()
                if client_secret:
                    yield PaymentState.create_order(
                        payment_method="stripe", payment_status="paid"
                    )
                else:
                    yield rx.toast.error(self.payment_error or "Payment failed")
            elif self.selected_payment_method == "cod":
                client_secret = await self.create_cod_advance_payment_intent()
                if client_secret:
                    yield PaymentState.create_order(
                        payment_method="cod", payment_status="partial"
                    )
                else:
                    yield rx.toast.error(self.payment_error or "COD advance failed")
        except Exception as e:
            logging.exception(f"Error processing payment: {e}")
            self.payment_error = f"Payment processing failed: {str(e)}"
            yield rx.toast.error(self.payment_error)
        finally:
            self.processing_payment = False

    @rx.event
    async def create_order(self, payment_method: str, payment_status: str):
        import datetime
        import uuid

        cart_state = await self.get_state(CartState)
        auth_state = await self.get_state(AuthState)
        product_state = await self.get_state(ProductState)
        order_id = f"DK{uuid.uuid4().hex[:8].upper()}"
        subtotal = cart_state.subtotal
        total_amount = await self.total_amount_computed
        new_order: Order = {
            "id": order_id,
            "user_email": auth_state.logged_in_user["email"],
            "items": cart_state.cart_items,
            "subtotal": subtotal,
            "shipping_cost": self.shipping_cost,
            "cod_advance": await self.cod_advance_amount
            if payment_method == "cod"
            else None,
            "cod_remaining": await self.cod_remaining_amount
            if payment_method == "cod"
            else None,
            "total_amount": total_amount,
            "payment_method": {
                "type": payment_method,
                "card_last4": None,
                "brand": None,
            },
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
        async with cart_state:
            cart_state.items = {}
        if product_state.strapi_health == "ok":
            self._sync_order_to_strapi(new_order)
        else:
            logging.warning("Skipping Strapi order sync: Strapi health is not 'ok'.")
        yield rx.toast.success("Order placed successfully!")
        yield rx.redirect("/account/orders")

    def _sync_order_to_strapi(self, order: Order):
        try:
            order_data = {
                "order_id_string": order["id"],
                "user_email": order["user_email"],
                "subtotal": order["subtotal"],
                "shipping_cost": order["shipping_cost"],
                "cod_advance": order["cod_advance"],
                "cod_remaining": order["cod_remaining"],
                "total_amount": order["total_amount"],
                "payment_method_type": order["payment_method"]["type"],
                "payment_status": order["payment_status"],
                "shipping_address": json.dumps(order["shipping_address"]),
                "status": order["status"],
                "created_at": order["created_at"],
                "stripe_payment_intent_id": order["stripe_payment_intent_id"],
                "items_json": json.dumps(
                    [
                        {
                            "id": item["product"]["id"],
                            "name": item["product"]["name"],
                            "quantity": item["quantity"],
                        }
                        for item in order["items"]
                    ]
                ),
            }
            headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
            response = requests.post(
                f"{STRAPI_URL}/api/orders",
                json={"data": order_data},
                headers=headers,
                timeout=10,
            )
            if response.status_code not in [200, 201]:
                logging.error(
                    f"Failed to sync order to Strapi. Status: {response.status_code}, Body: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            logging.exception(f"Exception during order sync to Strapi: {e}")