"""Rule-based support request classifier; it does not call generative models."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass
from typing import Literal


Category = Literal["ACCESS", "BUG", "FEATURE", "SECURITY"]
Priority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]


@dataclass(frozen=True)
class AnalysisResult:
    category: Category
    priority: Priority
    response: str
    requiresHumanReview: bool
    mode: Literal["traditional"] = "traditional"

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


_SIGNALS: dict[Category, tuple[str, ...]] = {
    "SECURITY": (
        "vulnerabilidad", "brecha de seguridad", "incidente de seguridad",
        "acceso no autorizado", "cuenta comprometida", "cuenta hackeada",
        "cuenta fue comprometida", "cuenta fue hackeada",
        "datos expuestos", "filtracion de datos", "robo de datos",
        "credenciales expuestas", "phishing", "malware", "ransomware",
        "ataque", "exploit", "inyeccion sql",
    ),
    "ACCESS": (
        "no puedo iniciar sesion", "no puedo acceder", "problema de inicio de sesion",
        "error al iniciar sesion", "contrasena", "restablecer mi clave",
        "cuenta bloqueada", "acceso a mi cuenta", "login", "iniciar sesion",
        "autenticacion", "mfa", "doble factor",
    ),
    "BUG": (
        "error", "bug", "falla", "fallo", "no funciona", "dejo de funcionar",
        "se cierra", "se bloquea", "crash", "excepcion", "pantalla en blanco",
        "no carga", "caido", "caida", "perdida de datos",
    ),
    "FEATURE": (
        "solicito una funcionalidad", "nueva funcionalidad", "nueva funcion",
        "me gustaria", "seria posible", "quisiera que", "agregar",
        "anadir", "incorporar", "integrar", "mejora", "funcionalidad",
        "feature request",
    ),
}

_SECURITY_CRITICAL = (
    "cuenta comprometida", "cuenta hackeada", "datos expuestos",
    "cuenta fue comprometida", "cuenta fue hackeada",
    "filtracion de datos", "robo de datos", "credenciales expuestas",
    "ransomware", "ataque activo",
)
_BUG_CRITICAL = (
    "caida total", "servicio caido", "produccion no disponible",
    "perdida de datos", "todos los usuarios afectados",
)
_BUG_HIGH = ("bloquea a varios usuarios", "varios usuarios afectados", "fallo en produccion")
_ACCESS_HIGH = (
    "todos los usuarios sin acceso", "autenticacion caida",
    "sistema de autenticacion no funciona",
)
_ACCESS_LOW = ("como puedo iniciar sesion", "como inicio sesion", "como cambiar mi contrasena")
_BUG_LOW = ("error visual", "detalle cosmetico", "error tipografico")
_AMBIGUOUS = ("no puedo trabajar", "necesito ayuda", "tengo un problema", "algo no funciona")

_RESPONSES: dict[Category, str] = {
    "ACCESS": (
        "Lamentamos el inconveniente. Verifica tus credenciales y utiliza la "
        "recuperación de contraseña si es necesario."
    ),
    "BUG": (
        "Gracias por reportarlo. Comparte los pasos para reproducir el problema "
        "y cualquier mensaje de error para que podamos investigarlo."
    ),
    "FEATURE": (
        "Gracias por la sugerencia. Registraremos la solicitud para que el equipo "
        "evalúe su utilidad y prioridad."
    ),
    "SECURITY": (
        "Gracias por alertarnos. El equipo de seguridad revisará el incidente; "
        "no compartas contraseñas ni datos sensibles en este canal."
    ),
}


def _normalize(message: str) -> str:
    decomposed = unicodedata.normalize("NFD", message.casefold())
    without_accents = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    return re.sub(r"\s+", " ", without_accents).strip()


def _matches(text: str, phrases: tuple[str, ...]) -> bool:
    return any(
        re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text)
        for phrase in phrases
    )


def _category(text: str) -> tuple[Category, bool]:
    # Security evidence always wins over competing labels or instructions in the message.
    if _matches(text, _SIGNALS["SECURITY"]):
        return "SECURITY", False

    scores = {
        category: sum(_matches(text, (phrase,)) for phrase in phrases)
        for category, phrases in _SIGNALS.items()
        if category != "SECURITY"
    }
    best_score = max(scores.values())
    if best_score == 0:
        return "BUG", True

    # Stable tie-break: access issue, system defect, then feature request.
    for category in ("ACCESS", "BUG", "FEATURE"):
        if scores[category] == best_score:
            return category, False
    raise AssertionError("A non-zero category score must select a category")


def _priority(category: Category, text: str, ambiguous: bool) -> Priority:
    if category == "SECURITY":
        return "CRITICAL" if _matches(text, _SECURITY_CRITICAL) else "HIGH"
    if ambiguous:
        return "MEDIUM"
    if category == "BUG":
        if _matches(text, _BUG_CRITICAL):
            return "CRITICAL"
        if _matches(text, _BUG_HIGH):
            return "HIGH"
        if _matches(text, _BUG_LOW):
            return "LOW"
        return "MEDIUM"
    if category == "ACCESS":
        if _matches(text, _ACCESS_HIGH):
            return "HIGH"
        if _matches(text, _ACCESS_LOW):
            return "LOW"
        return "MEDIUM"
    return "LOW"


def analyze_traditional(message: str) -> AnalysisResult:
    """Classify a support message using fixed lexical rules and templates."""
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not message.strip():
        raise ValueError("message must not be empty")

    text = _normalize(message)
    category, ambiguous = _category(text)
    priority = _priority(category, text, ambiguous)
    return AnalysisResult(
        category=category,
        priority=priority,
        response=_RESPONSES[category],
        requiresHumanReview=category == "SECURITY" or ambiguous or priority == "CRITICAL",
    )
