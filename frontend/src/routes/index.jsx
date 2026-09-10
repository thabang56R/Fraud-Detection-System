import { createFileRoute, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import Shell from "../components/Shell";
import { getRoot, getModelInfo } from "../lib/api";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "FinShield — Real-time Fraud Detection Platform" },
      {
        name: "description",
        content:
          "FinShield scores payments in real time using rules, supervised learning and anomaly detection, with drift monitoring for fintech risk teams.",
      },
      { property: "og:title", content: "FinShield — Real-time Fraud Detection Platform" },
      {
        property: "og:description",
        content: "Fraud scoring, feature transparency and model drift monitoring in one console.",
      },
    ],
  }),
  component: Overview,
});

const ENDPOINTS = [
  {
    title: "Hybrid scoring",
    body: "Rules, the supervised classifier and the anomaly detector are combined into one decision per transaction.",
    path: "POST /score/hybrid",
  },
  {
    title: "Feature transparency",
    body: "Realtime features derived from customer and merchant history are returned alongside every score.",
    path: "POST /features/realtime",
  },
  {
    title: "Policy inspection",
    body: "Run the deterministic rule set on its own to see which policy triggered and why.",
    path: "POST /rules/evaluate",
  },
  {
    title: "Drift monitoring",
    body: "Data and feature drift reports straight from the monitoring job — no notebooks required.",
    path: "GET /monitoring/report",
  },
];

function Overview() {
  const [root, setRoot] = useState(null);
  const [info, setInfo] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    getRoot()
      .then(setRoot)
      .catch((e) => setErr(e.message));
    getModelInfo()
      .then(setInfo)
      .catch(() => {});
  }, []);

  const meta = (info && info.supervised_model_metadata) || {};

  return (
    <Shell>
      <section className="fs-hero p-4 p-lg-5">
        <div className="row align-items-center g-4">
          <div className="col-lg-8">
            <p className="fs-label mb-2">
              FastAPI service · v{(root && root.version) || "0.7.0"} ·{" "}
              {(root && root.environment) || "local"}
            </p>
            <h1 className="text-ink fw-bold mb-3" style={{ maxWidth: "34ch" }}>
              Fraud decisions you can explain, in real time.
            </h1>
            <p className="text-subtle mb-4" style={{ maxWidth: "60ch" }}>
              FinShield is a production-style fraud detection platform for fintech. Submit a
              transaction and see the rule policy, the model probability and the anomaly score behind
              every verdict.
            </p>
            <div className="d-flex flex-wrap gap-2">
              <Link to="/console" className="btn btn-primary">
                Open scoring console
              </Link>
              <Link to="/monitoring" className="btn btn-outline-primary">
                View drift report
              </Link>
            </div>
          </div>
          <div className="col-lg-4">
            <ul className="list-unstyled mb-0 small">
              {["Rules engine", "Supervised classifier", "Anomaly detector", "Hybrid decision"].map(
                (s, i) => (
                  <li
                    key={s}
                    className="d-flex justify-content-between border-bottom py-2 text-subtle"
                  >
                    <span>{s}</span>
                    <span className="mono">{String(i + 1).padStart(2, "0")}</span>
                  </li>
                ),
              )}
            </ul>
          </div>
        </div>
      </section>

      {err ? (
        <div className="alert alert-warning mt-4 mb-0 small" role="alert">
          {err}
        </div>
      ) : null}

      <section className="row g-3 mt-4">
        {[
          { label: "Service", value: root ? "online" : err ? "offline" : "checking" },
          { label: "Model", value: meta.model_name || meta.model_type || "registry" },
          {
            label: "ROC AUC",
            value: meta.roc_auc ? Number(meta.roc_auc).toFixed(3) : meta.version || "—",
          },
          { label: "Scoring engines", value: "4" },
        ].map((s) => (
          <div className="col-6 col-lg-3" key={s.label}>
            <div className="fs-card h-100 p-3">
              <p className="fs-label mb-1">{s.label}</p>
              <p className="fs-stat mb-0 text-truncate">{s.value}</p>
            </div>
          </div>
        ))}
      </section>

      <h2 className="h5 text-ink mt-5 mb-3">What the platform exposes</h2>
      <section className="row g-3">
        {ENDPOINTS.map((c) => (
          <div className="col-md-6" key={c.title}>
            <article className="fs-card h-100 p-4">
              <h3 className="h6 text-ink">{c.title}</h3>
              <p className="text-subtle small mb-3">{c.body}</p>
              <code className="mono small text-primary">{c.path}</code>
            </article>
          </div>
        ))}
      </section>
    </Shell>
  );
}
