"""E-commerce example with product catalog and cart."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Card, Divider, Badge
from ontaic import Table, Modal, Toast, Navbar, Sidebar, SidebarLink
from ontaic import If, ForEach


class EcommerceApp(Component):
    """Main e-commerce application."""
    
    show_cart: bool = False
    show_checkout: bool = False
    notification: str = ""
    cart_items: str = "[]"
    
    def render(self):
        return Box(
            # Navbar
            Navbar(
                NavLink("/", "Home"),
                NavLink("/products", "Products"),
                NavLink("/about", "About"),
                brand="Ontaic Store",
                class_name="bg-white shadow-sm",
            ),
            
            # Main content
            Router(
                {
                    "/": HomePage(),
                    "/products": ProductsPage(),
                    "/product/1": ProductDetail(id=1),
                    "/cart": CartPage(),
                    "/checkout": CheckoutPage(),
                },
                initial_route="/",
            ),
            
            # Cart modal
            Modal(
                Text("Shopping Cart", tag="h3", class_name="text-lg font-semibold mb-4"),
                CartItems(),
                Button("Checkout", class_name="bg-blue-500 text-white px-4 py-2 rounded-lg"),
                title="Cart",
                is_open=self.show_cart,
                size="lg",
            ),
            
            # Toast notification
            Toast(
                message=self.notification,
                type="success",
                duration=3000,
            ) if self.notification else Text(""),
            
            class_name="min-h-screen bg-gray-100",
        )


class NavLink(Element):
    """Navigation link component."""
    
    def __init__(self, href: str, text: str, class_name: str = ""):
        self.href = href
        self.link_text = text
        super().__init__("a", class_name=class_name)

    def render(self):
        return f'<a href="{self.href}" class="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium">{self.link_text}</a>'


class Router(Element):
    """Simple router component."""
    
    def __init__(self, routes: dict, initial_route: str = "/", **kwargs):
        self.routes = routes
        self.initial_route = initial_route
        super().__init__("div", **kwargs)

    def render(self):
        routes_html = []
        for path, component in self.routes.items():
            if hasattr(component, "render"):
                content = component.render()
            else:
                content = str(component)
            routes_html.append(f'<div data-route="{path}" class="route-page">{content}</div>')
        
        return f"""<div id="router">
            {"".join(routes_html)}
            <script>
            (function() {{
                const router = document.getElementById('router');
                const pages = router.querySelectorAll('.route-page');
                
                function navigate(path) {{
                    pages.forEach(p => p.style.display = 'none');
                    const page = router.querySelector('[data-route="' + path + '"]');
                    if (page) page.style.display = 'block';
                    window.history.pushState({{}}, '', path);
                }}
                
                window.addEventListener('popstate', () => {{
                    navigate(window.location.pathname);
                }});
                
                navigate(window.location.pathname || '{self.initial_route}');
            }})();
            </script>
        </div>"""


class ProductCard(Element):
    """Product card component."""
    
    def __init__(self, product: dict, class_name: str = ""):
        self.product = product
        super().__init__("div", class_name=class_name)

    def render(self):
        return f"""<div class="bg-white rounded-lg shadow overflow-hidden hover:shadow-lg transition-shadow">
            <div class="aspect-w-1 aspect-h-1 bg-gray-200">
                <img src="{self.product.get('image', '')}" alt="{self.product.get('name', '')}" class="w-full h-48 object-cover">
            </div>
            <div class="p-4">
                <h3 class="text-lg font-semibold text-gray-900">{self.product.get('name', '')}</h3>
                <p class="text-gray-600 text-sm mt-1">{self.product.get('description', '')[:50]}...</p>
                <div class="flex items-center justify-between mt-4">
                    <span class="text-xl font-bold text-gray-900">${self.product.get('price', 0)}</span>
                    <button class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600" 
                        onclick="addToCart({self.product.get('id', 0)})">Add to Cart</button>
                </div>
            </div>
        </div>"""


class ProductDetail(Element):
    """Product detail component."""
    
    def __init__(self, id: int, **kwargs):
        self.product_id = id
        super().__init__("div", **kwargs)

    def render(self):
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-gray-200 rounded-lg h-96"></div>
                <div>
                    <h1 class="text-3xl font-bold text-gray-900">Product {self.product_id}</h1>
                    <p class="text-gray-600 mt-4">Product description goes here. This is a sample product from the Ontaic store.</p>
                    <div class="mt-6">
                        <span class="text-3xl font-bold text-gray-900">$99.99</span>
                    </div>
                    <div class="mt-6 space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Quantity</label>
                            <input type="number" min="1" value="1" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500">
                        </div>
                        <button class="w-full bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600" 
                            onclick="addToCart({self.product_id})">Add to Cart</button>
                        <button class="w-full bg-gray-100 text-gray-900 px-6 py-3 rounded-lg hover:bg-gray-200">
                            Add to Wishlist
                        </button>
                    </div>
                </div>
            </div>
        </div>"""


class CartItems(Element):
    """Cart items component."""
    
    def render(self):
        return f"""<div class="space-y-4">
            <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                <div class="w-16 h-16 bg-gray-200 rounded"></div>
                <div class="flex-1">
                    <h4 class="font-medium">Product 1</h4>
                    <p class="text-sm text-gray-600">$99.99</p>
                </div>
                <button class="text-red-500 hover:text-red-700">Remove</button>
            </div>
            <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                <div class="w-16 h-16 bg-gray-200 rounded"></div>
                <div class="flex-1">
                    <h4 class="font-medium">Product 2</h4>
                    <p class="text-sm text-gray-600">$49.99</p>
                </div>
                <button class="text-red-500 hover:text-red-700">Remove</button>
            </div>
            <div class="border-t pt-4 mt-4">
                <div class="flex justify-between font-semibold">
                    <span>Total:</span>
                    <span>$149.98</span>
                </div>
            </div>
        </div>"""


class HomePage(Element):
    """Home page component."""
    
    def render(self):
        products = [
            {"id": 1, "name": "Product 1", "price": 99.99, "image": "", "description": "Amazing product"},
            {"id": 2, "name": "Product 2", "price": 49.99, "image": "", "description": "Great value"},
            {"id": 3, "name": "Product 3", "price": 149.99, "image": "", "description": "Premium quality"},
        ]
        
        products_html = ""
        for product in products:
            products_html += ProductCard(product).render()
        
        return f"""<div class="max-w-7xl mx-auto py-8 px-4">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-gray-900">Welcome to Ontaic Store</h1>
                <p class="text-xl text-gray-600 mt-4">Discover our amazing products</p>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {products_html}
            </div>
        </div>"""


class ProductsPage(Element):
    """Products page component."""
    
    def render(self):
        products = [
            {"id": 1, "name": "Product 1", "price": 99.99, "image": "", "description": "Amazing product"},
            {"id": 2, "name": "Product 2", "price": 49.99, "image": "", "description": "Great value"},
            {"id": 3, "name": "Product 3", "price": 149.99, "image": "", "description": "Premium quality"},
            {"id": 4, "name": "Product 4", "price": 79.99, "image": "", "description": "Best seller"},
            {"id": 5, "name": "Product 5", "price": 129.99, "image": "", "description": "New arrival"},
            {"id": 6, "name": "Product 6", "price": 59.99, "image": "", "description": "On sale"},
        ]
        
        products_html = ""
        for product in products:
            products_html += ProductCard(product).render()
        
        return f"""<div class="max-w-7xl mx-auto py-8 px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">All Products</h1>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                {products_html}
            </div>
        </div>"""


class CartPage(Element):
    """Cart page component."""
    
    def render(self):
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>
            <div class="bg-white rounded-lg shadow p-6">
                {CartItems().render()}
                <div class="mt-6">
                    <button class="w-full bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600">
                        Proceed to Checkout
                    </button>
                </div>
            </div>
        </div>"""


class CheckoutPage(Element):
    """Checkout page component."""
    
    def render(self):
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-xl font-semibold mb-4">Shipping Information</h2>
                    <div class="space-y-4">
                        <input type="text" placeholder="Full Name" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <input type="email" placeholder="Email" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <input type="text" placeholder="Address" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <input type="text" placeholder="City" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                        <input type="text" placeholder="ZIP Code" class="w-full px-3 py-2 border border-gray-300 rounded-lg">
                    </div>
                </div>
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
                    <div class="space-y-4">
                        <div class="flex justify-between">
                            <span>Subtotal:</span>
                            <span>$149.98</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Shipping:</span>
                            <span>$9.99</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Tax:</span>
                            <span>$12.00</span>
                        </div>
                        <div class="border-t pt-4">
                            <div class="flex justify-between font-semibold text-lg">
                                <span>Total:</span>
                                <span>$171.97</span>
                            </div>
                        </div>
                    </div>
                    <button class="w-full bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 mt-6">
                        Place Order
                    </button>
                </div>
            </div>
        </div>"""


if __name__ == "__main__":
    app = EcommerceApp()
    print("E-commerce app created!")
    print("Run 'ontaic dev' to start the development server.")
