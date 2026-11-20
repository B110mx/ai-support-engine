import { MODES } from "./constants.js";
import { AppError } from "./errors.js";

const MAX_MESSAGE_LENGTH = 5000;

export function validateAnalyzeRequest(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    throw new AppError("El cuerpo debe ser un objeto JSON.", 400, "INVALID_BODY");
  }

  const { message, mode } = body;
  if (typeof message !== "string" || message.trim().length < 3) {
    throw new AppError("message debe ser un texto de al menos 3 caracteres.", 400, "INVALID_MESSAGE");
  }
  if (message.length > MAX_MESSAGE_LENGTH) {
    throw new AppError(`message no puede exceder ${MAX_MESSAGE_LENGTH} caracteres.`, 400, "MESSAGE_TOO_LONG");
  }
  if (!MODES.includes(mode)) {
    throw new AppError(`mode debe ser ${MODES.join(" o ")}.`, 400, "INVALID_MODE");
  }

  return { message: message.trim(), mode };
}
