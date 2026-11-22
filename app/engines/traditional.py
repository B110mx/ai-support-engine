"""Deterministic, rule-based support request engine."""

from __future__ import annotations

import re
import unicodedata

from app.domain.models import Category, EngineResult, Priority


_SIGNALS: dict[Category, tuple[str, ...]] = {
    Category.SECURITY: (
        "vulnerabilidad",
        "brecha de seguridad",
        "incidente de seguridad",
        "acceso no autorizado",
        "cuenta comprometida",
        "cuenta hackeada",
        "datos expuestos",
        "filtracion de datos",
        "robo de datos",
        "credenciales expuestas",
        "phishing",
        "malware",
        "ransomware",
        "ataque",
        "exploit",
        "inyeccion sql",
    ),
    Category.ACCESS: (
        "no puedo iniciar sesion",
        "no puedo acceder",
        "problema de inicio de sesion",
        "error al iniciar sesion",
        "contrasena",
        "restablecer mi clave",
        "cuenta bloqueada",
        "acceso a mi cuenta",
        "login",
        "iniciar sesion",
        "autenticacion",
        "todos los usuarios sin acceso",
        "autenticacion caida",
        "sistema de autenticacion no funciona",
        "mfa",
        "doble factor",
    ),
    Category.BUG: (
        "error",
        "bug",
        "falla",
        "fallo",
        "no funciona",
        "dejo de funcionar",
        "se cierra",
        "se bloquea",
        "crash",
        "excepcion",
        "pantalla en blanco",
        "no carga",
        "caido",
        "caida",
        "perdida de datos",
    ),
    Category.FEATURE: (
        "solicito una funcionalidad",
        "nueva funcionalidad",
        "nueva funcion",
        "me gustaria",
        "seria posible",
        "quisiera que",
        "agregar",
        "anadir",
        "incorporar",
        "integrar",
        "mejora",
        "funcionalidad",
        "feature request",
    ),
}

_SECURITY_CRITICAL = (
    "cuenta comprometida",
    "cuenta hackeada",
    "datos expuestos",
    "filtracion de datos",
    "robo de datos",
    "credenciales expuestas",
    "ransomware",
    "ataque activo",
)
_BUG_CRITICAL = (
    "caida total",
    "servicio caido",
    "produccion no disponible",
    "perdida de datos",
    "todos los usuarios afectados",
)
_BUG_HIGH = (
    "bloquea a varios usuarios",
    "varios usuarios afectados",
    "fallo en produccion",
)
_ACCESS_HIGH = (
    "todos los usuarios sin acceso",
    "autenticacion caida",
    "sistema de autenticacion no funciona",
)
_ACCESS_LOW = (
    "como puedo iniciar sesion",
    "como inicio sesion",
    "como cambiar mi contrasena",
)
_BUG_LOW = ("error visual", "detalle cosmetico", "error tipografico")

_RESPONSES: dict[Category, str] = {
    Category.ACCESS: (
        "Lamentamos el inconveniente. Verifica tus credenciales y utiliza la "
        "recuperación de contraseña si es necesario."
    ),
    Category.BUG: (
        "Gracias por reportarlo. Comparte los pasos para reproducir el problema "
        "y cualquier mensaje de error para que podamos investigarlo."
    ),
    Category.FEATURE: (
        "Gracias por la sugerencia. Registraremos la solicitud para que el equipo "
        "evalúe su utilidad y prioridad."
    ),
    Category.SECURITY: (
        "Gracias por alertarnos. El equipo de seguridad revisará el incidente; "
        "no compartas contraseñas ni datos sensibles en este canal."
    ),
}


def _normalize(message: str) -> str:
    decomposed = unicodedata.normalize("NFD", message.casefold())
    without_accents = "".join(
        character
        for character in decomposed
        if unicodedata.category(character) != "Mn"
    )
    return re.sub(r"\s+", " ", without_accents).strip()


def _matches(text: str, phrases: tuple[str, ...]) -> bool:
    return any(
        re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text)
        for phrase in phrases
    )


def _category(text: str) -> tuple[Category, bool]:
    if _matches(text, _SIGNALS[Category.SECURITY]):
        return Category.SECURITY, False

    scores = {
        category: sum(_matches(text, (phrase,)) for phrase in phrases)
        for category, phrases in _SIGNALS.items()
        if category is not Category.SECURITY
    }
    best_score = max(scores.values())
    if best_score == 0:
        return Category.BUG, True

    for category in (Category.ACCESS, Category.BUG, Category.FEATURE):
        if scores[category] == best_score:
            return category, False
    raise AssertionError("A non-zero score must select a category")


def _priority(category: Category, text: str, ambiguous: bool) -> Priority:
    if category is Category.SECURITY:
        return (
            Priority.CRITICAL
            if _matches(text, _SECURITY_CRITICAL)
            else Priority.HIGH
        )
    if ambiguous:
        return Priority.MEDIUM
    if category is Category.BUG:
        if _matches(text, _BUG_CRITICAL):
            return Priority.CRITICAL
        if _matches(text, _BUG_HIGH):
            return Priority.HIGH
        if _matches(text, _BUG_LOW):
            return Priority.LOW
        return Priority.MEDIUM
    if category is Category.ACCESS:
        if _matches(text, _ACCESS_HIGH):
            return Priority.HIGH
        if _matches(text, _ACCESS_LOW):
            return Priority.LOW
        return Priority.MEDIUM
    return Priority.LOW


def analyze_traditional(message: str) -> EngineResult:
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not message.strip():
        raise ValueError("message must not be empty")

    text = _normalize(message)
    category, ambiguous = _category(text)
    priority = _priority(category, text, ambiguous)
    return EngineResult(
        category=category,
        priority=priority,
        response=_RESPONSES[category],
        requiresHumanReview=(
            category is Category.SECURITY
            or ambiguous
            or priority is Priority.CRITICAL
        ),
    )


class TraditionalEngine:
    """Adapter that satisfies the shared SupportEngine protocol."""

    def analyze(self, message: str) -> EngineResult:
        return analyze_traditional(message)
