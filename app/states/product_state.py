import reflex as rx
from typing import TypedDict, Literal


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
    products: list[Product] = [
        {
            "id": 1,
            "name": "Artisan Leather Journal",
            "sku": "DK-LJ001",
            "price": 2499.0,
            "original_price": 2999.0,
            "description": "A beautifully crafted leather journal for those who love to write. Made with genuine leather and recycled paper.",
            "images": ["/placeholder.svg", "/placeholder.svg", "/placeholder.svg"],
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
            "images": ["/placeholder.svg", "/placeholder.svg"],
            "category": "Anniversary",
            "occasion": "Anniversary",
            "recipient": "For Her",
            "stock": 40,
            "rating": 4.9,
            "num_reviews": 250,
        },
        {
            "id": 3,
            "name": "Gourmet Chocolate Box",
            "sku": "DK-GCB003",
            "price": 1999.0,
            "original_price": None,
            "description": "An assortment of 16 handcrafted gourmet chocolates. A perfect treat for any occasion.",
            "images": ["/placeholder.svg", "/placeholder.svg"],
            "category": "Corporate",
            "occasion": "Corporate",
            "recipient": "For All",
            "stock": 15,
            "rating": 4.7,
            "num_reviews": 180,
        },
        {
            "id": 4,
            "name": "Engraved Silver Cufflinks",
            "sku": "DK-CUF004",
            "price": 4999.0,
            "original_price": 5499.0,
            "description": "Personalize these sterling silver cufflinks with initials for a timeless gift.",
            "images": ["/placeholder.svg", "/placeholder.svg"],
            "category": "Personalized",
            "occasion": "Anniversary",
            "recipient": "For Him",
            "stock": 10,
            "rating": 4.9,
            "num_reviews": 95,
        },
        {
            "id": 5,
            "name": "Plush Teddy Bear",
            "sku": "DK-TB005",
            "price": 1299.0,
            "original_price": None,
            "description": "A soft and cuddly teddy bear, perfect for kids and the young at heart.",
            "images": ["/placeholder.svg"],
            "category": "Birthday",
            "occasion": "Birthday",
            "recipient": "For Kids",
            "stock": 50,
            "rating": 4.6,
            "num_reviews": 75,
        },
        {
            "id": 6,
            "name": "Premium Tea Collection",
            "sku": "DK-TC006",
            "price": 2799.0,
            "original_price": None,
            "description": "A curated selection of the finest organic teas from around the world.",
            "images": ["/placeholder.svg", "/placeholder.svg"],
            "category": "Corporate",
            "occasion": "Corporate",
            "recipient": "For All",
            "stock": 30,
            "rating": 4.8,
            "num_reviews": 110,
        },
    ]
    selected_product: Product | None = None

    @rx.var
    def featured_products(self) -> list[Product]:
        return self.products[:4]

    @rx.var
    def categories(self) -> list[str]:
        return sorted(list(set((p["category"] for p in self.products))))

    @rx.event
    def get_product_details(self):
        product_id_str = self.router.page.params.get("product_id", "")
        if product_id_str.isdigit():
            product_id = int(product_id_str)
            self.selected_product = next(
                (p for p in self.products if p["id"] == product_id), None
            )
        else:
            self.selected_product = None

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