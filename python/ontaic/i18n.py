"""Internationalization (i18n) support for ontaic."""
import json
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Translation:
    """Translation for a single key."""
    key: str
    value: str
    context: Optional[str] = None


@dataclass
class Locale:
    """Locale configuration."""
    code: str
    name: str
    direction: str = "ltr"  # ltr or rtl
    decimal_separator: str = "."
    thousands_separator: str = ","
    date_format: str = "YYYY-MM-DD"
    time_format: str = "HH:mm"
    currency: str = "USD"
    currency_symbol: str = "$"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "direction": self.direction,
            "decimal_separator": self.decimal_separator,
            "thousands_separator": self.thousands_separator,
            "date_format": self.date_format,
            "time_format": self.time_format,
            "currency": self.currency,
            "currency_symbol": self.currency_symbol,
        }


# Predefined locales
LOCALES = {
    "en": Locale("en", "English", currency="USD", currency_symbol="$"),
    "es": Locale("es", "Español", currency="EUR", currency_symbol="€"),
    "fr": Locale("fr", "Français", currency="EUR", currency_symbol="€"),
    "de": Locale("de", "Deutsch", currency="EUR", currency_symbol="€"),
    "ja": Locale("ja", "日本語", currency="JPY", currency_symbol="¥"),
    "zh": Locale("zh", "中文", currency="CNY", currency_symbol="¥"),
    "ar": Locale("ar", "العربية", direction="rtl", currency="SAR", currency_symbol="﷼"),
    "he": Locale("he", "עברית", direction="rtl", currency="ILS", currency_symbol="₪"),
}


class I18n:
    """Internationalization manager."""
    
    def __init__(
        self,
        default_locale: str = "en",
        translations_dir: str = "translations",
    ):
        self.default_locale = default_locale
        self.current_locale: str = default_locale
        self.translations_dir = Path(translations_dir)
        self.translations: Dict[str, Dict[str, str]] = {}
        self.locales: Dict[str, Locale] = LOCALES.copy()
        self._interceptors: List[Callable] = []
        self._missing_handler: Optional[Callable] = None
        
        # Load translations
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files."""
        if not self.translations_dir.exists():
            return
        
        for file_path in self.translations_dir.glob("*.json"):
            locale_code = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations[locale_code] = json.load(f)
            except Exception as e:
                print(f"[ontaic-i18n] Failed to load {file_path}: {e}")
    
    def set_locale(self, locale: str):
        """Set the current locale."""
        if locale in self.translations or locale in LOCALES:
            self.current_locale = locale
            # Notify interceptors
            for interceptor in self._interceptors:
                interceptor(locale)
        else:
            print(f"[ontaic-i18n] Unknown locale: {locale}")
    
    def get_locale(self) -> str:
        """Get the current locale code."""
        return self.current_locale
    
    def get_locale_config(self) -> Locale:
        """Get the current locale configuration."""
        return self.locales.get(self.current_locale, LOCALES[self.default_locale])
    
    def t(self, key: str, **kwargs) -> str:
        """Translate a key with optional interpolation."""
        # Get translation
        translation = self._get_translation(key)
        
        # Apply interpolation
        if kwargs:
            for k, v in kwargs.items():
                translation = translation.replace(f"{{{k}}}", str(v))
        
        return translation
    
    def _get_translation(self, key: str) -> str:
        """Get translation for a key."""
        # Try current locale
        if self.current_locale in self.translations:
            if key in self.translations[self.current_locale]:
                return self.translations[self.current_locale][key]
        
        # Try default locale
        if self.default_locale in self.translations:
            if key in self.translations[self.default_locale]:
                return self.translations[self.default_locale][key]
        
        # Try fallback chain
        for locale_code, translations in self.translations.items():
            if key in translations:
                return translations[key]
        
        # Call missing handler
        if self._missing_handler:
            return self._missing_handler(key, self.current_locale)
        
        # Return key as fallback
        return key
    
    def add_translation(self, locale: str, key: str, value: str):
        """Add a translation."""
        if locale not in self.translations:
            self.translations[locale] = {}
        self.translations[locale][key] = value
    
    def add_translations(self, locale: str, translations: Dict[str, str]):
        """Add multiple translations."""
        if locale not in self.translations:
            self.translations[locale] = {}
        self.translations[locale].update(translations)
    
    def load_translations(self, locale: str, data: Dict[str, str]):
        """Load translations from a dictionary."""
        self.translations[locale] = data
    
    def save_translations(self, locale: str, file_path: str = None):
        """Save translations to a file."""
        if locale not in self.translations:
            return
        
        if file_path is None:
            self.translations_dir.mkdir(parents=True, exist_ok=True)
            file_path = self.translations_dir / f"{locale}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.translations[locale], f, ensure_ascii=False, indent=2)
    
    def get_available_locales(self) -> List[str]:
        """Get list of available locale codes."""
        return list(set(list(self.translations.keys()) + list(LOCALES.keys())))
    
    def get_locale_name(self, locale_code: str) -> str:
        """Get the name of a locale."""
        if locale_code in self.locales:
            return self.locales[locale_code].name
        return locale_code
    
    def format_number(self, number: float, locale: str = None) -> str:
        """Format a number according to locale."""
        locale_config = self.locales.get(locale or self.current_locale, LOCALES[self.default_locale])
        
        # Format with locale separators
        integer_part = int(number)
        decimal_part = number - integer_part
        
        # Format integer part with thousands separator
        integer_str = str(integer_part)
        if len(integer_str) > 3:
            parts = []
            for i in range(len(integer_str), 0, -3):
                parts.insert(0, integer_str[max(0, i-3):i])
            integer_str = locale_config.thousands_separator.join(parts)
        
        if decimal_part:
            decimal_str = f"{locale_config.decimal_separator}{int(decimal_part * 100)}"
            return f"{integer_str}{decimal_str}"
        
        return integer_str
    
    def format_currency(self, amount: float, locale: str = None) -> str:
        """Format a currency amount according to locale."""
        locale_config = self.locales.get(locale or self.current_locale, LOCALES[self.default_locale])
        formatted = self.format_number(amount, locale)
        return f"{locale_config.currency_symbol}{formatted}"
    
    def format_date(self, date_str: str, locale: str = None) -> str:
        """Format a date string according to locale."""
        locale_config = self.locales.get(locale or self.current_locale, LOCALES[self.default_locale])
        # Simple formatting - in production, use a date library
        return date_str
    
    def on_missing(self, handler: Callable):
        """Register a handler for missing translations."""
        self._missing_handler = handler
    
    def intercept(self, handler: Callable):
        """Register a locale change interceptor."""
        self._interceptors.append(handler)
    
    def generate_js_code(self) -> str:
        """Generate JavaScript code for i18n."""
        translations_json = json.dumps(self.translations, ensure_ascii=False)
        locales_json = {code: locale.to_dict() for code, locale in self.locales.items()}
        
        return f"""
        // i18n Manager
        const i18n = {{
            currentLocale: '{self.current_locale}',
            defaultLocale: '{self.default_locale}',
            translations: {translations_json},
            locales: {json.dumps(locales_json)},
            
            t(key, params = {{}}) {{
                let translation = this.translations[this.currentLocale]?.[key] 
                    || this.translations[this.defaultLocale]?.[key]
                    || key;
                
                // Apply interpolation
                Object.entries(params).forEach(([k, v]) => {{
                    translation = translation.replace(`{{${{k}}}}`, v);
                }});
                
                return translation;
            }},
            
            setLocale(locale) {{
                if (this.locales[locale]) {{
                    this.currentLocale = locale;
                    localStorage.setItem('ontaic-locale', locale);
                    document.documentElement.lang = locale;
                    document.documentElement.dir = this.locales[locale].direction;
                    document.dispatchEvent(new CustomEvent('localechange', {{ detail: locale }}));
                }}
            }},
            
            getLocale() {{
                return this.currentLocale;
            }},
            
            getLocaleConfig() {{
                return this.locales[this.currentLocale];
            }},
            
            formatNumber(number, locale) {{
                const config = this.locales[locale || this.currentLocale];
                return new Intl.NumberFormat(config.code).format(number);
            }},
            
            formatCurrency(amount, locale) {{
                const config = this.locales[locale || this.currentLocale];
                return new Intl.NumberFormat(config.code, {{
                    style: 'currency',
                    currency: config.currency
                }}).format(amount);
            }},
            
            formatDate(date, locale) {{
                const config = this.locales[locale || this.currentLocale];
                return new Intl.DateTimeFormat(config.code).format(new Date(date));
            }},
            
            init() {{
                const savedLocale = localStorage.getItem('ontaic-locale') || '{self.current_locale}';
                this.setLocale(savedLocale);
            }}
        }};
        
        // Initialize i18n
        i18n.init();
        """


# Locale selector component
class LocaleSelector:
    """Locale selector dropdown component."""
    
    def __init__(self, i18n: I18n = None):
        self.i18n = i18n or I18n()
    
    def render(self) -> str:
        locales = self.i18n.get_available_locales()
        options_html = "\n".join([
            f'<option value="{code}" {"selected" if code == self.i18n.current_locale else ""}>{self.i18n.get_locale_name(code)}</option>'
            for code in locales
        ])
        
        return f"""
        <select 
            onchange="i18n.setLocale(this.value)"
            class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
            {options_html}
        </select>
        """


# Translation component
class T:
    """Translation helper for templates."""
    
    def __init__(self, i18n: I18n = None):
        self.i18n = i18n or I18n()
    
    def __call__(self, key: str, **kwargs) -> str:
        return self.i18n.t(key, **kwargs)


# Example translations
ENGLISH_TRANSLATIONS = {
    "app.title": "My Application",
    "app.description": "Built with Ontaic",
    "nav.home": "Home",
    "nav.about": "About",
    "nav.contact": "Contact",
    "nav.login": "Login",
    "nav.logout": "Logout",
    "nav.profile": "Profile",
    "nav.settings": "Settings",
    "form.submit": "Submit",
    "form.cancel": "Cancel",
    "form.save": "Save",
    "form.delete": "Delete",
    "form.edit": "Edit",
    "form.create": "Create",
    "form.search": "Search",
    "form.filter": "Filter",
    "form.sort": "Sort",
    "form.reset": "Reset",
    "form.clear": "Clear",
    "form.close": "Close",
    "form.confirm": "Confirm",
    "form.yes": "Yes",
    "form.no": "No",
    "form.ok": "OK",
    "form.error": "Error",
    "form.success": "Success",
    "form.warning": "Warning",
    "form.info": "Info",
    "form.loading": "Loading...",
    "form.no_data": "No data available",
    "form.required": "This field is required",
    "form.invalid_email": "Invalid email address",
    "form.password_mismatch": "Passwords do not match",
    "user.greeting": "Hello, {name}!",
    "user.welcome": "Welcome back!",
    "user.logout_confirm": "Are you sure you want to logout?",
    "user.delete_confirm": "Are you sure you want to delete this user?",
    "cart.title": "Shopping Cart",
    "cart.empty": "Your cart is empty",
    "cart.total": "Total",
    "cart.checkout": "Checkout",
    "cart.add": "Add to Cart",
    "cart.remove": "Remove",
    "cart.quantity": "Quantity",
    "cart.price": "Price",
    "blog.title": "Blog",
    "blog.no_posts": "No posts available",
    "blog.read_more": "Read more",
    "blog.comments": "Comments",
    "blog.leave_comment": "Leave a comment",
    "blog.post_comment": "Post Comment",
    "dashboard.title": "Dashboard",
    "dashboard.welcome": "Welcome to your dashboard",
    "dashboard.stats": "Statistics",
    "dashboard.users": "Users",
    "dashboard.revenue": "Revenue",
    "dashboard.orders": "Orders",
    "dashboard.conversion": "Conversion",
}

SPANISH_TRANSLATIONS = {
    "app.title": "Mi Aplicación",
    "app.description": "Construido con Ontaic",
    "nav.home": "Inicio",
    "nav.about": "Acerca de",
    "nav.contact": "Contacto",
    "nav.login": "Iniciar sesión",
    "nav.logout": "Cerrar sesión",
    "nav.profile": "Perfil",
    "nav.settings": "Configuración",
    "form.submit": "Enviar",
    "form.cancel": "Cancelar",
    "form.save": "Guardar",
    "form.delete": "Eliminar",
    "form.edit": "Editar",
    "form.create": "Crear",
    "form.search": "Buscar",
    "form.filter": "Filtrar",
    "form.sort": "Ordenar",
    "form.reset": "Restablecer",
    "form.clear": "Limpiar",
    "form.close": "Cerrar",
    "form.confirm": "Confirmar",
    "form.yes": "Sí",
    "form.no": "No",
    "form.ok": "Aceptar",
    "form.error": "Error",
    "form.success": "Éxito",
    "form.warning": "Advertencia",
    "form.info": "Información",
    "form.loading": "Cargando...",
    "form.no_data": "No hay datos disponibles",
    "form.required": "Este campo es obligatorio",
    "form.invalid_email": "Correo electrónico inválido",
    "form.password_mismatch": "Las contraseñas no coinciden",
    "user.greeting": "¡Hola, {name}!",
    "user.welcome": "¡Bienvenido de vuelta!",
    "user.logout_confirm": "¿Estás seguro de que quieres cerrar sesión?",
    "user.delete_confirm": "¿Estás seguro de que quieres eliminar este usuario?",
    "cart.title": "Carrito de Compras",
    "cart.empty": "Tu carrito está vacío",
    "cart.total": "Total",
    "cart.checkout": "Pagar",
    "cart.add": "Añadir al Carrito",
    "cart.remove": "Eliminar",
    "cart.quantity": "Cantidad",
    "cart.price": "Precio",
    "blog.title": "Blog",
    "blog.no_posts": "No hay publicaciones disponibles",
    "blog.read_more": "Leer más",
    "blog.comments": "Comentarios",
    "blog.leave_comment": "Dejar un comentario",
    "blog.post_comment": "Publicar Comentario",
    "dashboard.title": "Panel de Control",
    "dashboard.welcome": "Bienvenido a tu panel de control",
    "dashboard.stats": "Estadísticas",
    "dashboard.users": "Usuarios",
    "dashboard.revenue": "Ingresos",
    "dashboard.orders": "Pedidos",
    "dashboard.conversion": "Conversión",
}

FRENCH_TRANSLATIONS = {
    "app.title": "Mon Application",
    "app.description": "Construit avec Ontaic",
    "nav.home": "Accueil",
    "nav.about": "À propos",
    "nav.contact": "Contact",
    "nav.login": "Connexion",
    "nav.logout": "Déconnexion",
    "nav.profile": "Profil",
    "nav.settings": "Paramètres",
    "form.submit": "Soumettre",
    "form.cancel": "Annuler",
    "form.save": "Enregistrer",
    "form.delete": "Supprimer",
    "form.edit": "Modifier",
    "form.create": "Créer",
    "form.search": "Rechercher",
    "form.filter": "Filtrer",
    "form.sort": "Trier",
    "form.reset": "Réinitialiser",
    "form.clear": "Effacer",
    "form.close": "Fermer",
    "form.confirm": "Confirmer",
    "form.yes": "Oui",
    "form.no": "Non",
    "form.ok": "OK",
    "form.error": "Erreur",
    "form.success": "Succès",
    "form.warning": "Avertissement",
    "form.info": "Information",
    "form.loading": "Chargement...",
    "form.no_data": "Aucune donnée disponible",
    "form.required": "Ce champ est obligatoire",
    "form.invalid_email": "Adresse e-mail invalide",
    "form.password_mismatch": "Les mots de passe ne correspondent pas",
    "user.greeting": "Bonjour, {name}!",
    "user.welcome": "Bon retour!",
    "user.logout_confirm": "Êtes-vous sûr de vouloir vous déconnecter?",
    "user.delete_confirm": "Êtes-vous sûr de vouloir supprimer cet utilisateur?",
    "cart.title": "Panier",
    "cart.empty": "Votre panier est vide",
    "cart.total": "Total",
    "cart.checkout": "Paiement",
    "cart.add": "Ajouter au Panier",
    "cart.remove": "Supprimer",
    "cart.quantity": "Quantité",
    "cart.price": "Prix",
    "blog.title": "Blog",
    "blog.no_posts": "Aucun article disponible",
    "blog.read_more": "Lire la suite",
    "blog.comments": "Commentaires",
    "blog.leave_comment": "Laisser un commentaire",
    "blog.post_comment": "Publier le commentaire",
    "dashboard.title": "Tableau de bord",
    "dashboard.welcome": "Bienvenue sur votre tableau de bord",
    "dashboard.stats": "Statistiques",
    "dashboard.users": "Utilisateurs",
    "dashboard.revenue": "Revenus",
    "dashboard.orders": "Commandes",
    "dashboard.conversion": "Conversion",
}
