import { flatten } from "../lib/api";

function fmt(v) {
  if (v === null || v === undefined) return "—";
  if (typeof v === "number") return Number.isInteger(v) ? String(v) : v.toFixed(4);
  if (typeof v === "boolean") return v ? "true" : "false";
  if (Array.isArray(v)) return v.length ? v.join(", ") : "—";
  return String(v);
}

export function KeyValueGrid({ data, columns = 2 }) {
  const rows = flatten(data);
  if (!rows.length) return <p className="text-subtle small mb-0">No data returned.</p>;
  return (
    <div className="row g-lg-4">
      {[...Array(columns)].map((_, col) => (
        <dl className={columns === 2 ? "col-lg-6 mb-0" : "col-12 mb-0"} key={col}>
          {rows
            .filter((_, i) => i % columns === col)
            .map(([k, v]) => (
              <div className="fs-kv" key={k}>
                <dt>{k.replace(/_/g, " ")}</dt>
                <dd>{fmt(v)}</dd>
              </div>
            ))}
        </dl>
      ))}
    </div>
  );
}

export default function JsonPanel({ title, value, open = false }) {
  return (
    <details className="fs-card p-3" open={open}>
      <summary className="fs-label" style={{ cursor: "pointer" }}>
        {title}
      </summary>
      <pre className="fs-pre mt-3">{JSON.stringify(value, null, 2)}</pre>
    </details>
  );
}
