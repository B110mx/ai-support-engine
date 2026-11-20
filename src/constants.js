export const CATEGORIES = ["ACCESS", "BUG", "FEATURE", "SECURITY"];
export const PRIORITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
export const MODES = ["traditional", "generative"];

export const RESPONSE_SCHEMA = {
  type: "OBJECT",
  properties: {
    category: { type: "STRING", enum: CATEGORIES },
    priority: { type: "STRING", enum: PRIORITIES },
    response: { type: "STRING" },
    requiresHumanReview: { type: "BOOLEAN" }
  },
  required: ["category", "priority", "response", "requiresHumanReview"]
};
