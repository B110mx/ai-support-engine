from dataclasses import dataclass
import unicodedata

from app.domain.models import AnalysisMode, AnalysisResult, Category, Priority


@dataclass(frozen=True)
class Rule:
    category: Category
    terms: tuple[str, ...]
    response: str


RULES = (
    Rule(
        Category.SECURITY,
        (
            "vulnerabilidad", "hack", "phishing", "malware", "ransomware",
            "credenciales expuestas", "datos filtrados", "acceso no autorizado",
            "token robado", "inyeccion sql",
        ),
        "Su reporte se marcó como posible incidente de seguridad. Un especialista lo revisará de inmediato. No comparta credenciales ni información sensible.",
    ),
    Rule(
        Category.ACCESS,
        (
            "iniciar sesion", "inicio de sesion", "login", "contrasena",
            "password", "cuenta bloqueada", "no puedo entrar", "autenticacion",
        ),
        "Lamentamos el inconveniente. Verifique sus credenciales y utilice la recuperación de contraseña si es necesario.",
    ),
    Rule(
        Category.FEATURE,
        (
            "nueva funcion", "nueva funcionalidad", "agregar", "anadir",
            "me gustaria", "seria util", "solicitud de funcion", "feature",
        ),
        "Gracias por su sugerencia. Registramos la solicitud para que el equipo de producto evalúe su viabilidad.",
    ),
    Rule(
        Category.BUG,
        (
            "error", "falla", "fallo", "no funciona", "se cierra",
            "pantalla en blanco", "excepcion", "bug", "lento", "incorrecto",
        ),
        "Lamentamos el problema. Registramos la falla; incluya los pasos para reproducirla y cualquier mensaje de error disponible.",
    ),
)

CRITICAL_TERMS = (
    "ransomware", "datos filtrados", "credenciales expuestas",
    "token robado", "acceso no autorizado",
)
HIGH_TERMS = (
    "urgente", "produccion", "todos los usuarios", "servicio caido",
    "vulnerabilidad", "phishing", "malware",
)
LOW_TERMS = ("sugerencia", "cuando puedan", "seria util", "me gustaria")


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def select_priority(text: str, category: Category) -> Priority:
    if contains_any(text, CRITICAL_TERMS):
        return Priority.CRITICAL
    if category is Category.SECURITY or contains_any(text, HIGH_TERMS):
        return Priority.HIGH
    if category is Category.FEATURE or contains_any(text, LOW_TERMS):
        return Priority.LOW
    return Priority.MEDIUM


def analyze_traditional(message: str) -> AnalysisResult:
    normalized = normalize(message)
    rule = next(
        (candidate for candidate in RULES if contains_any(normalized, candidate.terms)),
        next(candidate for candidate in RULES if candidate.category is Category.BUG),
    )
    return AnalysisResult(
        category=rule.category,
        priority=select_priority(normalized, rule.category),
        response=rule.response,
        requiresHumanReview=rule.category is Category.SECURITY,
        mode=AnalysisMode.TRADITIONAL,
    )
