import test from "node:test";
import assert from "node:assert/strict";
import { analyzeGenerative } from "../src/engines/generative.js";

test("valida y normaliza la respuesta estructurada del proveedor", async () => {
  const fetchImpl = async () => new Response(JSON.stringify({
    candidates: [{ content: { parts: [{ text: JSON.stringify({
      category: "SECURITY",
      priority: "HIGH",
      response: "Escalaremos el incidente.",
      requiresHumanReview: false
    }) }] } }]
  }), { status: 200, headers: { "content-type": "application/json" } });

  const result = await analyzeGenerative("Posible phishing", { apiKey: "test", fetchImpl });
  assert.equal(result.category, "SECURITY");
  assert.equal(result.requiresHumanReview, true);
  assert.equal(result.mode, "generative");
});
