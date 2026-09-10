const TONES = {
  safe: { color: "#1a7f4b", badge: "text-bg-success", label: "Low risk" },
  warn: { color: "#b57206", badge: "text-bg-warning", label: "Elevated risk" },
  danger: { color: "#b02a30", badge: "text-bg-danger", label: "High risk" },
  idle: { color: "#c3ccd4", badge: "text-bg-secondary", label: "No score yet" },
};

export function toneFor(score) {
  if (typeof score !== "number") return "idle";
  return score >= 0.7 ? "danger" : score >= 0.35 ? "warn" : "safe";
}

export default function RiskGauge({ score, decision, label = "Risk score" }) {
  const pct = typeof score === "number" ? Math.max(0, Math.min(1, score)) : null;
  const tone = TONES[toneFor(score)];

  return (
    <div>
      <div className="d-flex align-items-end justify-content-between mb-2">
        <span className="fs-label">{label}</span>
        <span className="mono fw-semibold" style={{ fontSize: "2rem", color: tone.color }}>
          {pct === null ? "—" : (pct * 100).toFixed(1)}
          {pct === null ? "" : <span className="fs-6 text-subtle">/100</span>}
        </span>
      </div>
      <div className="fs-meter">
        <span
          style={{
            width: `${pct === null ? 0 : Math.max(pct * 100, 1.5)}%`,
            backgroundColor: tone.color,
            transition: "width .4s ease",
          }}
        />
      </div>
      <div className="d-flex justify-content-between align-items-center mt-3">
        <span className={`badge ${tone.badge}`}>
          {decision ? String(decision).replace(/_/g, " ") : tone.label}
        </span>
        <span className="small text-subtle">Threshold bands: 35 / 70</span>
      </div>
    </div>
  );
}
