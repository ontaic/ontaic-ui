"""Blog example with posts and comments."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Card, Divider, Badge
from ontaic import Navbar, Sidebar, SidebarLink, Modal, Toast
from ontaic import If, ForEach


class BlogApp(Component):
    """Main blog application."""
    
    show_modal: bool = False
    notification: str = ""
    current_post: int = 0
    
    def render(self):
        return Box(
            # Navbar
            Navbar(
                NavLink("/", "Home"),
                NavLink("/posts", "Posts"),
                NavLink("/about", "About"),
                brand="Ontaic Blog",
                class_name="bg-white shadow-sm",
            ),
            
            # Main content
            Flex(
                # Main content area
                Router(
                    {
                        "/": HomePage(),
                        "/posts": PostsPage(),
                        "/post/1": PostDetail(id=1),
                        "/post/2": PostDetail(id=2),
                        "/post/3": PostDetail(id=3),
                        "/about": AboutPage(),
                    },
                    initial_route="/",
                ),
                
                # Sidebar
                Sidebar(
                    SidebarLink("/", "Home", icon=""),
                    SidebarLink("/posts", "Posts", icon=""),
                    SidebarLink("/about", "About", icon=""),
                    class_name="bg-gray-50 border-r w-64",
                ),
                
                class_name="flex",
            ),
            
            # New post modal
            Modal(
                Text("Create New Post", tag="h3", class_name="text-lg font-semibold mb-4"),
                Input(placeholder="Title", class_name="w-full px-3 py-2 border rounded-lg mb-3"),
                Input(placeholder="Content", class_name="w-full px-3 py-2 border rounded-lg mb-3 h-32"),
                Button("Publish", class_name="bg-blue-500 text-white px-4 py-2 rounded-lg"),
                title="New Post",
                is_open=self.show_modal,
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
        
        return f"""<div id="router" class="flex-1">
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


class PostCard(Element):
    """Post card component."""
    
    def __init__(self, post: dict, class_name: str = ""):
        self.post = post
        super().__init__("div", class_name=class_name)

    def render(self):
        return f"""<article class="bg-white rounded-lg shadow overflow-hidden hover:shadow-lg transition-shadow">
            <div class="p-6">
                <div class="flex items-center text-sm text-gray-500 mb-2">
                    <span>{self.post.get('date', '')}</span>
                    <span class="mx-2">•</span>
                    <span>{self.post.get('category', '')}</span>
                </div>
                <h2 class="text-xl font-bold text-gray-900 mb-2">
                    <a href="/post/{self.post.get('id', '')}" class="hover:text-blue-600">{self.post.get('title', '')}</a>
                </h2>
                <p class="text-gray-600 mb-4">{self.post.get('excerpt', '')}</p>
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div class="w-8 h-8 bg-gray-300 rounded-full"></div>
                        <span class="ml-2 text-sm text-gray-700">{self.post.get('author', '')}</span>
                    </div>
                    <a href="/post/{self.post.get('id', '')}" class="text-blue-600 hover:text-blue-800 text-sm font-medium">Read more →</a>
                </div>
            </div>
        </article>"""


class Comment(Element):
    """Comment component."""
    
    def __init__(self, comment: dict, class_name: str = ""):
        self.comment = comment
        super().__init__("div", class_name=class_name)

    def render(self):
        return f"""<div class="border-b border-gray-200 py-4 last:border-0">
            <div class="flex items-center mb-2">
                <div class="w-8 h-8 bg-gray-300 rounded-full"></div>
                <span class="ml-2 font-medium text-gray-900">{self.comment.get('author', '')}</span>
                <span class="ml-2 text-sm text-gray-500">{self.comment.get('date', '')}</span>
            </div>
            <p class="text-gray-700">{self.comment.get('content', '')}</p>
        </div>"""


class PostDetail(Element):
    """Post detail component."""
    
    def __init__(self, id: int, **kwargs):
        self.post_id = id
        super().__init__("div", **kwargs)

    def render(self):
        comments = [
            {"author": "User 1", "date": "2 hours ago", "content": "Great article!"},
            {"author": "User 2", "date": "1 hour ago", "content": "Thanks for sharing!"},
        ]
        
        comments_html = ""
        for comment in comments:
            comments_html += Comment(comment).render()
        
        return f"""<article class="max-w-3xl mx-auto py-8 px-4">
            <div class="bg-white rounded-lg shadow p-8">
                <div class="flex items-center text-sm text-gray-500 mb-4">
                    <span>January 1, 2024</span>
                    <span class="mx-2">•</span>
                    <span>Technology</span>
                </div>
                <h1 class="text-3xl font-bold text-gray-900 mb-4">Post Title {self.post_id}</h1>
                <div class="flex items-center mb-6">
                    <div class="w-10 h-10 bg-gray-300 rounded-full"></div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-900">Author Name</p>
                        <p class="text-sm text-gray-500">5 min read</p>
                    </div>
                </div>
                <div class="prose prose-lg max-w-none">
                    <p class="text-gray-700 mb-4">This is the content of post {self.post_id}. It contains interesting information about the topic.</p>
                    <p class="text-gray-700 mb-4">More content continues here with detailed explanations and examples.</p>
                    <p class="text-gray-700">Final thoughts and conclusion of the article.</p>
                </div>
                <div class="border-t mt-8 pt-8">
                    <h3 class="text-xl font-semibold mb-4">Comments ({len(comments)})</h3>
                    <div class="space-y-4">
                        {comments_html}
                    </div>
                    <div class="mt-6">
                        <textarea placeholder="Add a comment..." class="w-full px-3 py-2 border border-gray-300 rounded-lg" rows="3"></textarea>
                        <button class="mt-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">Post Comment</button>
                    </div>
                </div>
            </div>
        </article>"""


class HomePage(Element):
    """Home page component."""
    
    def render(self):
        posts = [
            {"id": 1, "title": "Getting Started with Ontaic", "excerpt": "Learn how to build modern web apps with Python.", "date": "Jan 1, 2024", "category": "Tutorial", "author": "John Doe"},
            {"id": 2, "title": "Advanced State Management", "excerpt": "Deep dive into state management patterns.", "date": "Jan 2, 2024", "category": "Advanced", "author": "Jane Smith"},
            {"id": 3, "title": "Building Real-time Apps", "excerpt": "Create real-time applications with WebSocket.", "date": "Jan 3, 2024", "category": "Tutorial", "author": "Bob Johnson"},
        ]
        
        posts_html = ""
        for post in posts:
            posts_html += PostCard(post).render()
        
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <div class="text-center mb-12">
                <h1 class="text-4xl font-bold text-gray-900">Ontaic Blog</h1>
                <p class="text-xl text-gray-600 mt-4">Thoughts on building modern web applications</p>
            </div>
            <div class="space-y-6">
                {posts_html}
            </div>
        </div>"""


class PostsPage(Element):
    """Posts page component."""
    
    def render(self):
        posts = [
            {"id": 1, "title": "Getting Started with Ontaic", "excerpt": "Learn how to build modern web apps with Python.", "date": "Jan 1, 2024", "category": "Tutorial", "author": "John Doe"},
            {"id": 2, "title": "Advanced State Management", "excerpt": "Deep dive into state management patterns.", "date": "Jan 2, 2024", "category": "Advanced", "author": "Jane Smith"},
            {"id": 3, "title": "Building Real-time Apps", "excerpt": "Create real-time applications with WebSocket.", "date": "Jan 3, 2024", "category": "Tutorial", "author": "Bob Johnson"},
            {"id": 4, "title": "Deployment Guide", "excerpt": "How to deploy your Ontaic app to production.", "date": "Jan 4, 2024", "category": "DevOps", "author": "Alice Brown"},
        ]
        
        posts_html = ""
        for post in posts:
            posts_html += PostCard(post).render()
        
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <h1 class="text-3xl font-bold text-gray-900 mb-8">All Posts</h1>
            <div class="space-y-6">
                {posts_html}
            </div>
        </div>"""


class AboutPage(Element):
    """About page component."""
    
    def render(self):
        return f"""<div class="max-w-4xl mx-auto py-8 px-4">
            <div class="bg-white rounded-lg shadow p-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-4">About Ontaic Blog</h1>
                <p class="text-gray-700 mb-4">This blog is built with Ontaic, a Python UI framework that compiles to WebAssembly.</p>
                <p class="text-gray-700 mb-4">Features:</p>
                <ul class="list-disc list-inside text-gray-700 mb-4">
                    <li>Client-side routing</li>
                    <li>State management</li>
                    <li>Real-time updates with WebSocket</li>
                    <li>Hot reload</li>
                </ul>
                <p class="text-gray-700">Built with Python and WebAssembly for maximum performance.</p>
            </div>
        </div>"""


if __name__ == "__main__":
    app = BlogApp()
    print("Blog app created!")
    print("Run 'ontaic dev' to start the development server.")
