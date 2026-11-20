import test from "node:test";
import assert from "node:assert/strict";
import { request } from "node:http";
import { createApp } from "../src/app.js";

async function withServer(run) {
  const server = createApp();
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  try {
    await run(`http://127.0.0.1:${server.address().port}`);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

function postJson(baseUrl, path, payload) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const body = JSON.stringify(payload);
    const req = request(url, {
      method: "POST",
      headers: { "content-type": "application/json", "content-length": Buffer.byteLength(body) }
    }, (res) => {
      let responseBody = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => { responseBody += chunk; });
      res.on("end", () => resolve({ status: res.statusCode, body: JSON.parse(responseBody) }));
    });
    req.on("error", reject);
    req.end(body);
  });
}

test("POST /api/analyze conserva el contrato", async () => {
  await withServer(async (baseUrl) => {
    const { status, body } = await postJson(baseUrl, "/api/analyze", { message: "La aplicación muestra un error", mode: "traditional" });
    assert.equal(status, 200);
    assert.deepEqual(Object.keys(body), ["category", "priority", "response", "requiresHumanReview", "mode"]);
  });
});

test("rechaza modos inválidos", async () => {
  await withServer(async (baseUrl) => {
    const { status } = await postJson(baseUrl, "/api/analyze", { message: "Tengo un problema", mode: "manual" });
    assert.equal(status, 400);
  });
});
