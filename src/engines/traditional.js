const rules = [
  {
    category: "SECURITY",
    terms: ["vulnerabilidad", "hack", "phishing", "malware", "ransomware", "credenciales expuestas", "datos filtrados", "acceso no autorizado", "token robado", "inyección sql"],
    response: "Su reporte se ha marcado como un posible incidente de seguridad y será revisado de inmediato por personal especializado. No comparta credenciales ni información sensible."
  },
  {
    category: "ACCESS",
    terms: ["iniciar sesión", "inicio de sesión", "login", "contraseña", "password", "cuenta bloqueada", "no puedo entrar", "acceso", "autenticación"],
    response: "Lamentamos el inconveniente. Verifique sus credenciales y utilice la recuperación de contraseña si es necesario."
  },
  {
    category: "FEATURE",
    terms: ["nueva función", "nueva funcionalidad", "agregar", "añadir", "me gustaría", "sería útil", "solicitud de función", "feature"],
    response: "Gracias por su sugerencia. Registramos la solicitud para que el equipo de producto evalúe su viabilidad."
  },
  {
    category: "BUG",
    terms: ["error", "falla", "fallo", "no funciona", "se cierra", "pantalla en blanco", "excepción", "bug", "lento", "incorrecto"],
    response: "Lamentamos el problema. Registramos la falla para su diagnóstico; incluya los pasos para reproducirla y cualquier mensaje de error disponible."
  }
];

const criticalTerms = ["ransomware", "datos filtrados", "credenciales expuestas", "token robado", "acceso no autorizado"];
const highTerms = ["urgente", "producción", "todos los usuarios", "servicio caído", "vulnerabilidad", "phishing", "malware"];
const lowTerms = ["sugerencia", "cuando puedan", "sería útil", "me gustaría"];

function includesAny(text, terms) {
  return terms.some((term) => text.includes(term));
}

function priorityFor(text, category) {
  if (includesAny(text, criticalTerms)) return "CRITICAL";
  if (category === "SECURITY" || includesAny(text, highTerms)) return "HIGH";
  if (category === "FEATURE" || includesAny(text, lowTerms)) return "LOW";
  return "MEDIUM";
}

export function analyzeTraditional(message) {
  const normalized = message.toLocaleLowerCase("es");
  const matchedRule = rules.find((rule) => includesAny(normalized, rule.terms)) ?? rules.find((rule) => rule.category === "BUG");
  const category = matchedRule.category;

  return {
    category,
    priority: priorityFor(normalized, category),
    response: matchedRule.response,
    requiresHumanReview: category === "SECURITY",
    mode: "traditional"
  };
}
