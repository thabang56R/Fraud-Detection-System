const STORAGE_KEY = "finshield.api.base";
const DEFAULT_BASE = "http://127.0.0.1:8000";

export function getApiBase() {
  if (typeof window === "undefined") return DEFAULT_BASE;
  return window.localStorage.getItem(STORAGE_KEY) || DEFAULT_BASE;
}

export function setApiBase(url) {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, url.replace(/\/+$/, ""));
}

async function request(path, options) {
  const base = getApiBase().replace(/\/+$/, "");
  let res;
  try {
    res = await fetch(base + path, options);
  } catch (err) {
    throw new Error(
      `Cannot reach the FinShield API at ${base}. Start it with "uvicorn apps.api.main:app --reload" and allow CORS for this origin.`,
    );
  }
  const text = await res.text();
  let body = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { raw: text };
  }
  if (!res.ok) {
    const detail = body && body.detail ? JSON.stringify(body.detail) : res.statusText;
    throw new Error(`${res.status} ${detail}`);
  }
  return body;
}

export const getHealth = () => request("/health");
export const getRoot = () => request("/");
export const getModelInfo = () => request("/model/info");
export const getMonitoringReport = () => request("/monitoring/report");

const post = (path, payload) =>
  request(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

export const scoreHybrid = (p) => post("/score/hybrid", p);
export const scoreRules = (p) => post("/score/rules", p);
export const scoreModel = (p) => post("/score/model", p);
export const scoreAnomaly = (p) => post("/score/anomaly", p);
export const evaluateRules = (p) => post("/rules/evaluate", p);
export const realtimeFeatures = (p) => post("/features/realtime", p);

export const SCORE_ENGINES = [
  { id: "hybrid", label: "Hybrid", call: scoreHybrid, blurb: "Rules + supervised + anomaly" },
  { id: "model", label: "Supervised", call: scoreModel, blurb: "Gradient model probability" },
  { id: "anomaly", label: "Anomaly", call: scoreAnomaly, blurb: "Unsupervised outlier score" },
  { id: "rules", label: "Rules", call: scoreRules, blurb: "Deterministic risk policy" },
];

export function sampleTransaction() {
  return {
    transaction_id: "txn_" + Math.random().toString(36).slice(2, 10),
    customer_id: "cust_00184",
    merchant_id: "merch_2291",
    amount: 4820.5,
    currency: "ZAR",
    country: "ZA",
    device_type: "mobile",
    ip_address: "102.132.44.19",
    timestamp: new Date().toISOString(),
  };
}

// ---------------------------------------------------------------------------
// Demo mode: local simulation when the FastAPI backend is unreachable.
// ---------------------------------------------------------------------------

function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967295;
}

function demoSignals(p) {
  const signals = [];
  const amount = Number(p.amount) || 0;
  if (amount > 4000) signals.push(["amount_above_4000", 0.25]);
  else if (amount > 1500) signals.push(["amount_above_1500", 0.12]);
  if (p.country && p.country !== "ZA") signals.push(["foreign_country", 0.18]);
  if (p.device_type === "atm") signals.push(["atm_channel", 0.1]);
  const hour = new Date(p.timestamp || Date.now()).getUTCHours();
  if (hour >= 0 && hour <= 5) signals.push(["off_hours_00_05", 0.15]);
  return signals;
}

/** Simulate an engine response locally so the UI is testable without the API. */
export function simulateScore(engine, payload) {
  const jitter = hashSeed(JSON.stringify(payload) + engine) * 0.14;
  const signals = demoSignals(payload);
  const rulesScore = Math.min(signals.reduce((a, [, w]) => a + w, 0), 1);
  const modelScore = Math.min(rulesScore * 0.8 + jitter, 1);
  const anomalyScore = Math.min(jitter * 2.4 + signals.length * 0.09, 1);
  let score;
  if (engine === "rules") score = rulesScore;
  else if (engine === "model") score = modelScore;
  else if (engine === "anomaly") score = anomalyScore;
  else score = Math.min(0.45 * rulesScore + 0.35 * modelScore + 0.2 * anomalyScore + 0.04, 1);
  const decision = score >= 0.65 ? "BLOCK" : score >= 0.35 ? "REVIEW" : "APPROVE";
  return Promise.resolve({
    engine,
    demo: true,
    message: "Demo mode — simulated locally, backend not contacted.",
    result: {
      final_score: Number(score.toFixed(3)),
      decision,
      rules_score: Number(rulesScore.toFixed(3)),
      model_score: Number(modelScore.toFixed(3)),
      anomaly_score: Number(anomalyScore.toFixed(3)),
      triggered_rules: signals.map(([name]) => name),
    },
  });
}

export function simulateRules(payload) {
  const signals = demoSignals(payload);
  return Promise.resolve({
    rules_result: {
      demo: true,
      triggered: signals.map(([name]) => name),
      rule_count: signals.length,
      verdict: signals.length >= 3 ? "high_risk" : signals.length > 0 ? "medium_risk" : "low_risk",
    },
  });
}

export function simulateFeatures(payload) {
  const seed = hashSeed(JSON.stringify(payload));
  return Promise.resolve({
    features: {
      demo: true,
      amount_zscore: Number((seed * 4 - 1).toFixed(3)),
      customer_txn_count_24h: Math.round(seed * 9),
      customer_avg_amount_30d: Number((seed * 900 + 120).toFixed(2)),
      merchant_risk_rate: Number((seed * 0.4).toFixed(3)),
      device_seen_before: seed > 0.5,
      ip_velocity_1h: Math.round(seed * 14),
    },
  });
}

/** Pull a 0..1 risk figure out of whatever shape the engine returned. */
export function extractScore(result) {
  if (!result || typeof result !== "object") return null;
  const keys = [
    "final_score",
    "hybrid_score",
    "fraud_probability",
    "risk_score",
    "anomaly_score",
    "score",
  ];
  for (const k of keys) {
    const v = result[k];
    if (typeof v === "number") return v > 1 ? Math.min(v / 100, 1) : v;
  }
  return null;
}

export function extractDecision(result) {
  if (!result || typeof result !== "object") return null;
  return (
    result.decision || result.final_decision || result.action || result.risk_level || result.label || null
  );
}

export function flatten(obj, prefix = "") {
  const out = [];
  if (!obj || typeof obj !== "object") return out;
  for (const [k, v] of Object.entries(obj)) {
    const key = prefix ? `${prefix}.${k}` : k;
    if (v && typeof v === "object" && !Array.isArray(v)) out.push(...flatten(v, key));
    else out.push([key, v]);
  }
  return out;
}
