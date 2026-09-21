"""Portfolio example with projects and skills."""
from ontaic import Component, Box, Text, Button, Input, Container, Flex, Stack, Card, Divider, Badge
from ontaic import Navbar, Sidebar, SidebarLink, Modal, Toast
from ontaic import If, ForEach


class PortfolioApp(Component):
    """Main portfolio application."""
    
    show_modal: bool = False
    notification: str = ""
    
    def render(self):
        return Box(
            # Navbar
            Navbar(
                NavLink("/", "Home"),
                NavLink("/projects", "Projects"),
                NavLink("/skills", "Skills"),
                NavLink("/contact", "Contact"),
                brand="John Doe",
                class_name="bg-white shadow-sm",
            ),
            
            # Main content
            Router(
                {
                    "/": HomePage(),
                    "/projects": ProjectsPage(),
                    "/skills": SkillsPage(),
                    "/contact": ContactPage(),
                },
                initial_route="/",
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


class ProjectCard(Element):
    """Project card component."""
    
    def __init__(self, project: dict, class_name: str = ""):
        self.project = project
        super().__init__("div", class_name=class_name)

    def render(self):
        badges_html = ""
        for tech in self.project.get('tech', []):
            badges_html += f'<span class="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">{tech}</span>'
        
        return f"""<div class="bg-white rounded-lg shadow overflow-hidden hover:shadow-lg transition-shadow">
            <div class="h-48 bg-gradient-to-br from-blue-500 to-purple-600"></div>
            <div class="p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-2">{self.project.get('title', '')}</h3>
                <p class="text-gray-600 mb-4">{self.project.get('description', '')}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                    {badges_html}
                </div>
                <div class="flex gap-2">
                    <a href="{self.project.get('demo', '#')}" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 text-sm">Demo</a>
                    <a href="{self.project.get('github', '#')}" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 text-sm">GitHub</a>
                </div>
            </div>
        </div>"""


class SkillBar(Element):
    """Skill bar component."""
    
    def __init__(self, name: str, level: int, class_name: str = ""):
        self.name = name
        self.level = level
        super().__init__("div", class_name=class_name)

    def render(self):
        return f"""<div class="mb-4">
            <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-gray-700">{self.name}</span>
                <span class="text-sm text-gray-500">{self.level}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full transition-all duration-500" style="width: {self.level}%"></div>
            </div>
        </div>"""


class HomePage(Element):
    """Home page component."""
    
    def render(self):
        return f"""<div class="max-w-6xl mx-auto py-16 px-4">
            <!-- Hero Section -->
            <div class="text-center mb-16">
                <div class="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-6"></div>
                <h1 class="text-5xl font-bold text-gray-900 mb-4">John Doe</h1>
                <p class="text-xl text-gray-600 mb-6">Full Stack Developer</p>
                <p class="text-gray-600 max-w-2xl mx-auto mb-8">
                    Passionate about building beautiful, functional, and user-friendly applications.
                    I love working with modern technologies and solving complex problems.
                </p>
                <div class="flex justify-center gap-4">
                    <a href="/projects" class="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">View Projects</a>
                    <a href="/contact" class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50">Contact Me</a>
                </div>
            </div>
            
            <!-- Featured Projects -->
            <div class="mb-16">
                <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">Featured Projects</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {ProjectCard({
                        "title": "E-commerce Platform",
                        "description": "A full-featured e-commerce platform with cart, checkout, and payment integration.",
                        "tech": ["Python", "React", "PostgreSQL"],
                        "demo": "#",
                        "github": "#"
                    }).render()}
                    {ProjectCard({
                        "title": "Task Management App",
                        "description": "A collaborative task management application with real-time updates.",
                        "tech": ["Vue.js", "Node.js", "MongoDB"],
                        "demo": "#",
                        "github": "#"
                    }).render()}
                </div>
            </div>
            
            <!-- Skills Preview -->
            <div class="text-center">
                <h2 class="text-3xl font-bold text-gray-900 mb-8">Skills</h2>
                <div class="flex flex-wrap justify-center gap-4">
                    <span class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full">Python</span>
                    <span class="px-4 py-2 bg-green-100 text-green-800 rounded-full">JavaScript</span>
                    <span class="px-4 py-2 bg-purple-100 text-purple-800 rounded-full">React</span>
                    <span class="px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full">Node.js</span>
                    <span class="px-4 py-2 bg-red-100 text-red-800 rounded-full">PostgreSQL</span>
                    <span class="px-4 py-2 bg-indigo-100 text-indigo-800 rounded-full">Docker</span>
                </div>
            </div>
        </div>"""


class ProjectsPage(Element):
    """Projects page component."""
    
    def render(self):
        projects = [
            {
                "title": "E-commerce Platform",
                "description": "A full-featured e-commerce platform with cart, checkout, and payment integration.",
                "tech": ["Python", "React", "PostgreSQL"],
                "demo": "#",
                "github": "#"
            },
            {
                "title": "Task Management App",
                "description": "A collaborative task management application with real-time updates.",
                "tech": ["Vue.js", "Node.js", "MongoDB"],
                "demo": "#",
                "github": "#"
            },
            {
                "title": "Blog Platform",
                "description": "A modern blog platform with markdown support and SEO optimization.",
                "tech": ["Next.js", "TypeScript", "Prisma"],
                "demo": "#",
                "github": "#"
            },
            {
                "title": "Weather App",
                "description": "A beautiful weather application with location-based forecasts.",
                "tech": ["React", "OpenWeather API", "Tailwind"],
                "demo": "#",
                "github": "#"
            },
            {
                "title": "Portfolio Website",
                "description": "This portfolio website built with Ontaic.",
                "tech": ["Python", "Ontaic", "Tailwind"],
                "demo": "#",
                "github": "#"
            },
            {
                "title": "Chat Application",
                "description": "Real-time chat application with rooms and direct messaging.",
                "tech": ["Socket.io", "Express", "React"],
                "demo": "#",
                "github": "#"
            },
        ]
        
        projects_html = ""
        for project in projects:
            projects_html += ProjectCard(project).render()
        
        return f"""<div class="max-w-6xl mx-auto py-16 px-4">
            <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">Projects</h1>
            <p class="text-gray-600 text-center mb-12">A collection of my work and side projects</p>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {projects_html}
            </div>
        </div>"""


class SkillsPage(Element):
    """Skills page component."""
    
    def render(self):
        skills = {
            "Frontend": [
                {"name": "React", "level": 90},
                {"name": "Vue.js", "level": 85},
                {"name": "TypeScript", "level": 80},
                {"name": "Tailwind CSS", "level": 95},
            ],
            "Backend": [
                {"name": "Python", "level": 95},
                {"name": "Node.js", "level": 85},
                {"name": "PostgreSQL", "level": 80},
                {"name": "MongoDB", "level": 75},
            ],
            "DevOps": [
                {"name": "Docker", "level": 80},
                {"name": "AWS", "level": 70},
                {"name": "CI/CD", "level": 75},
                {"name": "Linux", "level": 85},
            ],
        }
        
        skills_html = ""
        for category, skill_list in skills.items():
            skill_bars = ""
            for skill in skill_list:
                skill_bars += SkillBar(skill["name"], skill["level"]).render()
            
            skills_html += f"""
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-xl font-bold text-gray-900 mb-4">{category}</h3>
                {skill_bars}
            </div>
            """
        
        return f"""<div class="max-w-6xl mx-auto py-16 px-4">
            <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">Skills</h1>
            <p class="text-gray-600 text-center mb-12">Technologies and tools I work with</p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                {skills_html}
            </div>
        </div>"""


class ContactPage(Element):
    """Contact page component."""
    
    def render(self):
        return f"""<div class="max-w-4xl mx-auto py-16 px-4">
            <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">Contact</h1>
            <p class="text-gray-600 text-center mb-12">Get in touch with me</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="bg-white rounded-lg shadow p-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Send a Message</h2>
                    <form class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                            <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                            <input type="email" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Message</label>
                            <textarea rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
                        </div>
                        <button type="submit" class="w-full px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">Send Message</button>
                    </form>
                </div>
                
                <div class="bg-white rounded-lg shadow p-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-6">Contact Info</h2>
                    <div class="space-y-4">
                        <div class="flex items-center">
                            <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                                <span class="text-blue-600">📧</span>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500">Email</p>
                                <p class="text-gray-900">john@example.com</p>
                            </div>
                        </div>
                        <div class="flex items-center">
                            <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-4">
                                <span class="text-green-600">📍</span>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500">Location</p>
                                <p class="text-gray-900">San Francisco, CA</p>
                            </div>
                        </div>
                        <div class="flex items-center">
                            <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center mr-4">
                                <span class="text-purple-600">💼</span>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500">Availability</p>
                                <p class="text-gray-900">Open to opportunities</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-8">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">Social Links</h3>
                        <div class="flex gap-4">
                            <a href="#" class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200">
                                <span>GitHub</span>
                            </a>
                            <a href="#" class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200">
                                <span>LinkedIn</span>
                            </a>
                            <a href="#" class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center hover:bg-gray-200">
                                <span>Twitter</span>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>"""


if __name__ == "__main__":
    app = PortfolioApp()
    print("Portfolio app created!")
    print("Run 'ontaic dev' to start the development server.")
