import reflex as rx
from typing import TypedDict, Literal
import logging
import os
import requests

STRAPI_URL = os.getenv(
    "STRAPI_URL", "https://committed-treasure-916aeef9fd.strapiapp.com/"
)
STRAPI_API_TOKEN = os.getenv(
    "STRAPI_API_TOKEN",
    "29c56c8d922ac739a56215545ff19501b2aa79b777294f7e212247861bd5102db96c808a4cd74223a8c5fcedbf045705a38d511857880968d194d64a040ea9dca7485a986f06f56d6e092ea1e1939409e933adbdf26057e8accb13ce0ef2994532e6b24e5f935fa32df69b9b02e3545e9af691096710e062cee2538b508756f8",
)
STRAPI_CONFIGURED = bool(STRAPI_URL and STRAPI_API_TOKEN)


class Product(TypedDict):
    id: int
    name: str
    sku: str
    price: float
    original_price: float | None
    description: str
    images: list[str]
    category: str
    occasion: str
    recipient: Literal["For Him", "For Her", "For Kids", "For All"]
    stock: int
    rating: float
    num_reviews: int


class ProductState(rx.State):
    products: list[Product] = []
    categories_from_strapi: list[str] = []
    selected_product: Product | None = None
    strapi_health: Literal["ok", "error", "misconfigured", "unknown"] = "unknown"
    _dummy_products: list[Product] = [
        {
            "id": 1,
            "name": "Artisan Leather Journal",
            "sku": "DK-LJ001",
            "price": 2499.0,
            "original_price": 2999.0,
            "description": "A beautifully crafted leather journal for those who love to write. Made with genuine leather and recycled paper.",
            "images": ["/placeholder.svg"],
            "category": "Personalized",
            "occasion": "Birthday",
            "recipient": "For All",
            "stock": 25,
            "rating": 4.8,
            "num_reviews": 120,
        },
        {
            "id": 2,
            "name": "Luxury Scented Candle Set",
            "sku": "DK-CS002",
            "price": 3499.0,
            "original_price": None,
            "description": "A set of three hand-poured soy wax candles in luxurious scents: Lavender, Sandalwood, and Citrus.",
            "images": ["/placeholder.svg"],
            "category": "Anniversary",
            "occasion": "Anniversary",
            "recipient": "For Her",
            "stock": 40,
            "rating": 4.9,
            "num_reviews": 250,
        },
    ]
    _dummy_categories: list[str] = [
        "Personalized",
        "Anniversary",
        "Corporate",
        "Birthday",
    ]

    @rx.event
    def on_load(self):
        return ProductState.run_strapi_health_check

    @rx.event
    def run_strapi_health_check(self):
        if not STRAPI_CONFIGURED:
            self.strapi_health = "misconfigured"
            self.products = self._dummy_products
            self.categories_from_strapi = self._dummy_categories
            yield rx.toast.warning(
                "Strapi is not configured. Using dummy data.",
                description="Please set STRAPI_URL and STRAPI_API_TOKEN.",
                duration=5000,
            )
            return
        try:
            headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
            response = requests.get(
                f"{STRAPI_URL}/api/categories", headers=headers, timeout=5
            )
            if response.status_code == 200:
                self.strapi_health = "ok"
                yield [
                    ProductState.fetch_products_from_strapi,
                    ProductState.fetch_categories_from_strapi,
                ]
            else:
                self.strapi_health = "error"
                self.products = self._dummy_products
                self.categories_from_strapi = self._dummy_categories
                logging.error(
                    f"Strapi health check failed. Status: {response.status_code}, Body: {response.text}"
                )
                yield rx.toast.error(
                    "Strapi Connection Error",
                    description=f"Failed to connect to Strapi. Status: {response.status_code}",
                    duration=5000,
                )
        except requests.exceptions.RequestException as e:
            self.strapi_health = "error"
            self.products = self._dummy_products
            self.categories_from_strapi = self._dummy_categories
            logging.exception(f"Strapi health check failed with exception: {e}")
            yield rx.toast.error(
                "Strapi Connection Failed",
                description="Could not reach Strapi server. Using dummy data.",
                duration=5000,
            )

    @rx.event
    def fetch_products_from_strapi(self):
        try:
            headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
            response = requests.get(
                f"{STRAPI_URL}/api/products?populate=*", headers=headers, timeout=10
            )
            if response.status_code == 200:
                strapi_products = response.json()["data"]
                self.products = [
                    self._transform_strapi_product(p) for p in strapi_products
                ]
            elif response.status_code == 404:
                logging.warning(
                    "Strapi 'products' endpoint not found (404). Falling back to dummy data."
                )
                self.products = self._dummy_products
                yield rx.toast.warning(
                    "Products endpoint not found. Please create 'Product' collection in Strapi.",
                    duration=5000,
                )
            else:
                logging.error(
                    f"Failed to fetch products from Strapi. Status: {response.status_code}, Body: {response.text}"
                )
                self.products = self._dummy_products
                yield rx.toast.error(
                    f"Could not fetch products (Status: {response.status_code}).",
                    duration=5000,
                )
        except requests.exceptions.RequestException as e:
            logging.exception(f"Failed to fetch products from Strapi: {e}")
            self.products = self._dummy_products
            yield rx.toast.error(
                "Network error while fetching products.", duration=5000
            )

    @rx.event
    def fetch_categories_from_strapi(self):
        try:
            headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
            response = requests.get(
                f"{STRAPI_URL}/api/categories", headers=headers, timeout=10
            )
            if response.status_code == 200:
                data = response.json().get("data", [])
                self.categories_from_strapi = [
                    cat.get("name", cat.get("attributes", {}).get("name"))
                    for cat in data
                ]
            else:
                logging.warning(
                    f"Could not fetch categories (Status: {response.status_code}). Using fallback."
                )
                self.categories_from_strapi = self._dummy_categories
        except requests.exceptions.RequestException as e:
            logging.exception(f"Failed to fetch categories from Strapi: {e}")
            self.categories_from_strapi = self._dummy_categories

    def _transform_strapi_product(self, strapi_product: dict) -> Product:
        attrs = strapi_product.get("attributes", strapi_product)
        image_data = attrs.get("images", {}).get("data", [])
        images = []
        if image_data:
            for img in image_data:
                img_attrs = img.get("attributes", img)
                url = img_attrs.get("url")
                if url:
                    images.append(
                        f"{STRAPI_URL.rstrip('/')}{url}" if url.startswith("/") else url
                    )
        if not images:
            images.append("/placeholder.svg")
        return {
            "id": strapi_product["id"],
            "name": attrs.get("name", "N/A"),
            "sku": attrs.get("sku", "N/A"),
            "price": float(attrs.get("price", 0)),
            "original_price": float(attrs.get("original_price"))
            if attrs.get("original_price") is not None
            else None,
            "description": attrs.get("description", ""),
            "images": images,
            "category": attrs.get("category", "Uncategorized"),
            "occasion": attrs.get("occasion", "General"),
            "recipient": attrs.get("recipient", "For All"),
            "stock": int(attrs.get("stock", 0)),
            "rating": float(attrs.get("rating", 0.0)),
            "num_reviews": int(attrs.get("num_reviews", 0)),
        }

    @rx.var
    def featured_products(self) -> list[Product]:
        return self.products[:4]

    @rx.var
    def best_selling_products(self) -> list[Product]:
        if not self.products:
            return []
        return sorted(self.products, key=lambda p: p["num_reviews"], reverse=True)[:3]

    @rx.event
    def create_product(self, form_data: dict):
        if self.strapi_health != "ok":
            yield rx.toast.error("Strapi is not available. Cannot create product.")
            return
        payload = {
            "data": {
                "name": form_data["name"],
                "sku": form_data["sku"],
                "price": float(form_data["price"]),
                "description": form_data["description"],
                "category": form_data["category"],
                "stock": int(form_data["stock"]),
                "rating": 0.0,
                "num_reviews": 0,
            }
        }
        if form_data.get("original_price"):
            payload["data"]["original_price"] = float(form_data["original_price"])
        try:
            headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
            response = requests.post(
                f"{STRAPI_URL}/api/products", json=payload, headers=headers, timeout=10
            )
            if response.status_code in [200, 201]:
                yield rx.toast.success("Product created successfully in Strapi!")
                yield ProductState.fetch_products_from_strapi
            else:
                error_details = (
                    response.json().get("error", {}).get("message", "Unknown error")
                )
                logging.error(
                    f"Strapi error on product creation: {error_details} | Body: {response.text}"
                )
                yield rx.toast.error(f"Strapi error: {error_details}")
        except requests.exceptions.RequestException as e:
            logging.exception(f"Failed to create product in Strapi: {e}")
            yield rx.toast.error(f"Network error: Failed to create product: {e}")

    @rx.var
    def categories(self) -> list[str]:
        if self.strapi_health == "ok" and self.categories_from_strapi:
            return self.categories_from_strapi
        if self.strapi_health != "ok" or not self.products:
            return self._dummy_categories
        unique_categories = sorted(list(set((p["category"] for p in self.products))))
        return unique_categories if unique_categories else self._dummy_categories

    @rx.event
    def get_product_details(self):
        product_id_str = self.router.page.params.get("product_id", "")
        if not product_id_str.isdigit():
            self.selected_product = None
            return
        product_id = int(product_id_str)
        if self.strapi_health == "ok":
            try:
                headers = {"Authorization": f"Bearer {STRAPI_API_TOKEN}"}
                response = requests.get(
                    f"{STRAPI_URL}/api/products/{product_id}?populate=*",
                    headers=headers,
                    timeout=10,
                )
                if response.status_code == 200:
                    self.selected_product = self._transform_strapi_product(
                        response.json()["data"]
                    )
                else:
                    self.selected_product = None
                    yield rx.toast.error(f"Product with ID {product_id} not found.")
            except requests.exceptions.RequestException as e:
                logging.exception(f"Failed to get product details: {e}")
                self.selected_product = None
                yield rx.toast.error("Network error fetching product details.")
        else:
            self.selected_product = next(
                (p for p in self.products if p["id"] == product_id), None
            )

    @rx.var
    def current_category_name(self) -> str:
        return self.router.page.params.get("category_name", "all").replace("-", " ")

    @rx.var
    def products_in_category(self) -> list[Product]:
        category_name = self.current_category_name
        if category_name == "all":
            return self.products
        return [
            p
            for p in self.products
            if p["category"].lower().replace(" ", "-") == category_name
        ]