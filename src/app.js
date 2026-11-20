import { createServer } from "node:http";
import { analyzeSupportRequest } from "./analyze.js";
import { AppError } from "./errors.js";
import { validateAnalyzeRequest } from "./validation.js";

const MAX_BODY_BYTES = 16_384;

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, { "content-type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload));
}

async function readJson(request) {
  let body = "";
  for await (const chunk of request) {
    body += chunk;
    if (Buffer.byteLength(body) > MAX_BODY_BYTES) {
      throw new AppError("El cuerpo de la petición es demasiado grande.", 413, "BODY_TOO_LARGE");
    }
  }
  try {
    return JSON.parse(body || "{}");
  } catch {
    throw new AppError("El cuerpo contiene JSON inválido.", 400, "INVALID_JSON");
  }
}

export function createApp(options = {}) {
  return createServer(async (request, response) => {
    try {
      if (request.method === "GET" && request.url === "/health") {
        return sendJson(response, 200, { status: "ok" });
      }
      if (request.method === "POST" && request.url === "/api/analyze") {
        const input = validateAnalyzeRequest(await readJson(request));
        const result = await analyzeSupportRequest(input, options.generative);
        return sendJson(response, 200, result);
      }
      return sendJson(response, 404, { error: { code: "NOT_FOUND", message: "Ruta no encontrada." } });
    } catch (error) {
      const appError = error instanceof AppError ? error : new AppError("Error interno del servidor.");
      return sendJson(response, appError.statusCode, { error: { code: appError.code, message: appError.message } });
    }
  });
}
