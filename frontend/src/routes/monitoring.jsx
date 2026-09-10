import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import Shell from "../components/Shell";
import JsonPanel, { KeyValueGrid } from "../components/JsonPanel";
import { getMonitoringReport, flatten } from "../lib/api";

export const Route = createFileRoute("/monitoring")({
  head: () => ({
    meta: [
      { title: "Drift Monitoring — FinShield Fraud Detection" },
      {
        name: "description",
        content:
          "Population and feature drift report from the FinShield monitoring job, surfaced for risk and ML operations teams.",
      },
      { property: "og:title", content: "Drift Monitoring — FinShield" },
      {
        property: "og:description",
        content: "Feature drift and data health signals for the fraud detection models.",
      },
    ],
  }),
  component: Monitoring,
});

function DriftBar({ name, value }) {
  const v = Math.max(0, Math.min(1, Number(value) || 0));
  const color = v >= 0.3 ? "#b02a30" : v >= 0.1 ? "#b57206" : "#1a7f4b";
  return (
    <div className="col-md-6">
      <div className="d-flex justify-content-between small">
        <span className="text-subtle">{name.replace(/_/g, " ")}</span>
        <span className="mono text-ink">{v.toFixed(4)}</span>
      </div>
      <div className="fs-meter mt-1">
        <span style={{ width: `${Math.max(v * 100, 1.5)}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function Monitoring() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    setError(null);
    getMonitoringReport()
      .then(setReport)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const numeric = flatten(report).filter(
    ([k, v]) => typeof v === "number" && /drift|psi|score|ratio|rate/i.test(k),
  );

  return (
    <Shell>
      <div className="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-4">
        <div>
          <h1 className="h3 text-ink mb-1">Drift monitoring</h1>
          <p className="text-subtle mb-0" style={{ maxWidth: "62ch" }}>
            Output of the monitoring job comparing live traffic against the training reference window.
          </p>
        </div>
        <button className="btn btn-outline-primary" onClick={load} disabled={loading}>
          {loading ? "Refreshing…" : "Refresh report"}
        </button>
      </div>

      {error ? (
        <div className="alert alert-danger small" role="alert">
          {error}
        </div>
      ) : null}

      {numeric.length ? (
        <section className="fs-card p-4">
          <p className="fs-label mb-3">Drift signals</p>
          <div className="row g-3">
            {numeric.map(([k, v]) => (
              <DriftBar key={k} name={k} value={v} />
            ))}
          </div>
        </section>
      ) : null}

      {report ? (
        <>
          <section className="fs-card p-4 mt-4">
            <h2 className="h6 text-ink mb-3">Report detail</h2>
            <KeyValueGrid data={report} />
          </section>
          <div className="mt-4">
            <JsonPanel title="Raw monitoring payload" value={report} />
          </div>
        </>
      ) : !error ? (
        <p className="text-subtle small">Loading monitoring report…</p>
      ) : null}
    </Shell>
  );
}
