import { analyzeGenerative } from "./engines/generative.js";
import { analyzeTraditional } from "./engines/traditional.js";

export async function analyzeSupportRequest({ message, mode }, options = {}) {
  if (mode === "traditional") return analyzeTraditional(message);
  return analyzeGenerative(message, options);
}
