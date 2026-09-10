import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { getApiBase, setApiBase, getHealth } from "../lib/api";

const NAV = [
  { to: "/", label: "Overview" },
  { to: "/console", label: "Scoring console" },
  { to: "/monitoring", label: "Monitoring" },
  { to: "/model", label: "Models" },
];

function ApiStatus() {
  const [base, setBase] = useState("");
  const [draft, setDraft] = useState("");
  const [state, setState] = useState("checking");
  const [editing, setEditing] = useState(false);

  const probe = () => {
    setState("checking");
    getHealth()
      .then(() => setState("online"))
      .catch(() => setState("offline"));
  };

  useEffect(() => {
    const b = getApiBase();
    setBase(b);
    setDraft(b);
    probe();
  }, []);

  const save = (e) => {
    e.preventDefault();
    setApiBase(draft);
    setBase(draft.replace(/\/+$/, ""));
    setEditing(false);
    probe();
  };

  const badge =
    state === "online" ? "text-bg-success" : state === "offline" ? "text-bg-danger" : "text-bg-secondary";

  if (editing) {
    return (
      <form className="d-flex gap-2" onSubmit={save}>
        <input
          className="form-control form-control-sm mono"
          style={{ minWidth: "14rem" }}
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          spellCheck={false}
        />
        <button className="btn btn-sm btn-primary" type="submit">
          Save
        </button>
      </form>
    );
  }

  return (
    <button
      type="button"
      className="btn btn-sm btn-outline-secondary d-flex align-items-center gap-2"
      onClick={() => setEditing(true)}
      title="Change the API base URL"
    >
      <span className={`badge rounded-pill ${badge}`}>{state}</span>
      <span className="mono small">{base.replace(/^https?:\/\//, "")}</span>
    </button>
  );
}

export default function Shell({ children }) {
  return (
    <div className="d-flex flex-column min-vh-100">
      <nav className="fs-navbar sticky-top">
        <div className="container py-2 d-flex flex-wrap align-items-center gap-3">
          <Link to="/" className="d-flex align-items-center gap-2 text-decoration-none">
            <span className="fs-brand-mark">FS</span>
            <span className="fw-bold text-ink">FinShield</span>
          </Link>
          <div className="d-flex flex-wrap align-items-center gap-1">
            {NAV.map((item) => (
              <Link
                key={item.to}
                to={item.to}
                activeOptions={{ exact: item.to === "/" }}
                activeProps={{ className: "fs-navlink active" }}
                inactiveProps={{ className: "fs-navlink" }}
              >
                {item.label}
              </Link>
            ))}
          </div>
          <div className="ms-auto">
            <ApiStatus />
          </div>
        </div>
      </nav>

      <main className="container py-4 py-lg-5 flex-grow-1">{children}</main>

      <footer className="border-top bg-white mt-auto">
        <div className="container py-3 d-flex flex-wrap justify-content-between gap-2 small text-subtle">
          <span>FinShield Fraud Detection Platform — FastAPI scoring service v0.7.0</span>
          <span className="mono">rules · supervised · anomaly · hybrid</span>
        </div>
      </footer>
    </div>
  );
}
