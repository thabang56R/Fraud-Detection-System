import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import Shell from "../components/Shell";
import RiskGauge from "../components/RiskGauge";
import JsonPanel, { KeyValueGrid } from "../components/JsonPanel";
import {
  SCORE_ENGINES,
  sampleTransaction,
  extractScore,
  extractDecision,
  evaluateRules,
  realtimeFeatures,
} from "../lib/api";

export const Route = createFileRoute("/console")({
  head: () => ({
    meta: [
      { title: "Scoring Console — FinShield Fraud Detection" },
      {
        name: "description",
        content:
          "Submit a transaction and compare rules, supervised, anomaly and hybrid fraud scores with the full feature output.",
      },
      { property: "og:title", content: "Scoring Console — FinShield" },
      {
        property: "og:description",
        content: "Interactive fraud scoring against the FinShield API.",
      },
    ],
  }),
  component: Console,
});

const FIELDS = [
  { name: "transaction_id", label: "Transaction ID" },
  { name: "customer_id", label: "Customer ID" },
  { name: "merchant_id", label: "Merchant ID" },
  { name: "amount", label: "Amount", type: "number" },
  { name: "currency", label: "Currency" },
  { name: "country", label: "Country" },
  { name: "device_type", label: "Device", options: ["mobile", "web", "pos", "atm", "tablet"] },
  { name: "ip_address", label: "IP address" },
  { name: "timestamp", label: "Timestamp" },
];

function Console() {
  const [form, setForm] = useState(sampleTransaction);
  const [engine, setEngine] = useState("hybrid");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);
  const [features, setFeatures] = useState(null);
  const [rules, setRules] = useState(null);
  const [showPayload, setShowPayload] = useState(false);
  const [notice, setNotice] = useState(null);

  const update = (name) => (e) => setForm({ ...form, [name]: e.target.value });

  const loadSample = () => {
    const next = sampleTransaction();
    setForm(next);
    setShowPayload(true);
    setNotice(`Sample transaction ${next.transaction_id} loaded into the form.`);
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    setFeatures(null);
    setRules(null);
    const payload = { ...form, amount: Number(form.amount) };
    try {
      const def = SCORE_ENGINES.find((s) => s.id === engine);
      const data = await def.call(payload);
      setResponse(data);
      const [f, r] = await Promise.allSettled([
        data && data.features ? Promise.resolve({ features: data.features }) : realtimeFeatures(payload),
        evaluateRules(payload),
      ]);
      if (f.status === "fulfilled") setFeatures(f.value.features);
      if (r.status === "fulfilled") setRules(r.value.rules_result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const result = response ? (response.result ?? response) : null;
  const score = extractScore(result);
  const decision = extractDecision(result);

  return (
    <Shell>
      <div className="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-4">
        <div>
          <h1 className="h3 text-ink mb-1">Scoring console</h1>
          <p className="text-subtle mb-0" style={{ maxWidth: "62ch" }}>
            Build a transaction payload and route it through any of the four scoring engines.
          </p>
        </div>
        <div className="d-flex gap-2">
          <button className="btn btn-outline-primary" onClick={loadSample} type="button">
            Load sample transaction
          </button>
          <button
            className="btn btn-outline-secondary"
            type="button"
            onClick={() => setShowPayload((v) => !v)}
            aria-expanded={showPayload}
          >
            {showPayload ? "Hide payload" : "View payload"}
          </button>
        </div>
      </div>

      {notice ? (
        <div className="alert alert-info d-flex justify-content-between align-items-center small" role="status">
          <span>{notice}</span>
          <button type="button" className="btn-close" aria-label="Dismiss" onClick={() => setNotice(null)} />
        </div>
      ) : null}

      {showPayload ? (
        <div className="mb-4">
          <JsonPanel title="Request payload" value={{ ...form, amount: Number(form.amount) }} open />
        </div>
      ) : null}

      <div className="row g-4">
        <div className="col-lg-7">
          <form className="fs-card p-4" onSubmit={submit}>
            <p className="fs-label mb-2">Engine</p>
            <div className="row g-2">
              {SCORE_ENGINES.map((s) => (
                <div className="col-sm-6" key={s.id}>
                  <button
                    type="button"
                    className={`fs-engine h-100 ${engine === s.id ? "selected" : ""}`}
                    onClick={() => setEngine(s.id)}
                  >
                    <span className="d-block fw-semibold text-ink small">{s.label}</span>
                    <span className="d-block text-subtle" style={{ fontSize: ".8rem" }}>
                      {s.blurb}
                    </span>
                  </button>
                </div>
              ))}
            </div>

            <hr className="my-4" />

            <div className="row g-3">
              {FIELDS.map((f) => (
                <div className="col-sm-6" key={f.name}>
                  <label className="form-label fs-label" htmlFor={f.name}>
                    {f.label}
                  </label>
                  {f.options ? (
                    <select
                      id={f.name}
                      className="form-select mono"
                      value={form[f.name]}
                      onChange={update(f.name)}
                    >
                      {f.options.map((o) => (
                        <option key={o} value={o}>
                          {o}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      id={f.name}
                      className="form-control mono"
                      type={f.type || "text"}
                      step="0.01"
                      value={form[f.name]}
                      onChange={update(f.name)}
                      spellCheck={false}
                    />
                  )}
                </div>
              ))}
            </div>

            <button className="btn btn-primary w-100 mt-4" type="submit" disabled={loading}>
              {loading ? "Scoring…" : "Score transaction"}
            </button>

            {error ? (
              <div className="alert alert-danger small mt-3 mb-0" role="alert">
                {error}
              </div>
            ) : null}
          </form>
        </div>

        <div className="col-lg-5">
          <div className="fs-card p-4">
            <RiskGauge score={score} decision={decision} label={`${engine} score`} />
            <p className="small text-subtle mt-3 mb-0">
              {(response && response.message) || "Submit a transaction to get a score."}
            </p>
          </div>

          {result ? (
            <div className="fs-card p-4 mt-3">
              <p className="fs-label mb-2">Engine output</p>
              <KeyValueGrid data={result} columns={1} />
            </div>
          ) : null}

          {rules ? (
            <div className="fs-card p-4 mt-3">
              <p className="fs-label mb-2">Rule policy</p>
              <KeyValueGrid data={rules} columns={1} />
            </div>
          ) : null}
        </div>
      </div>

      {features ? (
        <section className="fs-card p-4 mt-4">
          <h2 className="h6 text-ink">Realtime features</h2>
          <p className="small text-subtle">
            Derived from customer and merchant transaction history at request time.
          </p>
          <KeyValueGrid data={features} />
        </section>
      ) : null}

      {response ? (
        <div className="mt-4">
          <JsonPanel title="Raw API response" value={response} />
        </div>
      ) : null}
    </Shell>
  );
}
