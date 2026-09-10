import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import Shell from "../components/Shell";
import JsonPanel, { KeyValueGrid } from "../components/JsonPanel";
import { getModelInfo } from "../lib/api";

export const Route = createFileRoute("/model")({
  head: () => ({
    meta: [
      { title: "Model Registry — FinShield Fraud Detection" },
      {
        name: "description",
        content:
          "Metadata for the supervised fraud classifier and the anomaly detector serving FinShield scoring traffic.",
      },
      { property: "og:title", content: "Model Registry — FinShield" },
      {
        property: "og:description",
        content: "Versions, metrics and training metadata for the deployed fraud models.",
      },
    ],
  }),
  component: ModelRegistry,
});

function ModelCard({ title, subtitle, data }) {
  const tag = data && (data.version || (data.trained_at ? "trained" : null));
  return (
    <div className="col-lg-6">
      <section className="fs-card h-100 p-4">
        <div className="d-flex justify-content-between align-items-start gap-3">
          <div>
            <h2 className="h6 text-ink mb-1">{title}</h2>
            <p className="small text-subtle mb-0">{subtitle}</p>
          </div>
          <span className="badge text-bg-light border mono">{tag || "registry"}</span>
        </div>
        <hr />
        <KeyValueGrid data={data} columns={1} />
      </section>
    </div>
  );
}

function ModelRegistry() {
  const [info, setInfo] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getModelInfo()
      .then(setInfo)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <Shell>
      <h1 className="h3 text-ink mb-1">Models</h1>
      <p className="text-subtle" style={{ maxWidth: "62ch" }}>
        Registry metadata for the two models behind the hybrid decision engine.
      </p>

      {error ? (
        <div className="alert alert-danger small" role="alert">
          {error}
        </div>
      ) : null}

      <div className="row g-4 mt-2">
        <ModelCard
          title="Supervised classifier"
          subtitle="Labelled fraud probability estimator"
          data={info && info.supervised_model_metadata}
        />
        <ModelCard
          title="Anomaly detector"
          subtitle="Unsupervised outlier scoring on realtime features"
          data={info && info.anomaly_model_metadata}
        />
      </div>

      {info ? (
        <div className="mt-4">
          <JsonPanel title="Raw /model/info response" value={info} />
        </div>
      ) : null}
    </Shell>
  );
}
