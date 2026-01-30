import React, { CSSProperties, useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./AuditLogsComponent.css";

interface Props {
  id: string;
  title?: string;
  styles?: CSSProperties;
  dataBinding?: {
    endpoint: string;
  };
}

/* ---------------------------------------
 * Display-only label normalization
 * ------------------------------------- */
const payloadLabelMap: Record<string, string> = {
  Comments: "Comment",
};

/* ---------------------------------------
 * Resolve CREATED AT correctly
 * ------------------------------------- */
const resolveCreatedAt = (row: any): string => {
  const ts =
    row.payload?.TimeStamp ||
    row.payload?.timestamp ||
    row.payload?.created_at;

  // Business / domain timestamp
  if (typeof ts === "string") {
    const d = new Date(ts);
    if (!isNaN(d.getTime())) {
      return d.toLocaleString();
    }
  }

  // Ledger fallback (explicit, never converted)
  if (row.created_at) {
    return `ledger#${row.created_at}`;
  }

  return "";
};

export const AuditLogsComponent: React.FC<Props> = ({
  id,
  title = "Logs",
  styles,
  dataBinding,
}) => {
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [limit, setLimit] = useState(25);
  const [offset, setOffset] = useState(0);

  const endpoint = dataBinding?.endpoint;
  const backendBase =
    process.env.REACT_APP_API_URL || "http://localhost:8000";

  /* ---------------------------------------
   * Fetch + normalize audit logs
   * ------------------------------------- */
  useEffect(() => {
    if (!endpoint) return;

    setLoading(true);

    const url =
      (endpoint.startsWith("/") ? backendBase : "") +
      endpoint +
      `?limit=${limit}&offset=${offset}`;

    axios
      .get(url)
      .then((res) => {
        const normalized = (Array.isArray(res.data) ? res.data : []).map(
          (row) => {
            let payload = row.payload;

            if (typeof payload === "string") {
              try {
                payload = JSON.parse(payload);
              } catch {
                payload = {};
              }
            }

            return {
              ...row,
              payload: payload && typeof payload === "object" ? payload : {},
            };
          }
        );

        setRows(normalized);
      })
      .catch(() => setError("Failed to load audit logs"))
      .finally(() => setLoading(false));
  }, [endpoint, backendBase, limit, offset]);

  /* ---------------------------------------
   * Compute dynamic payload columns
   * ------------------------------------- */
  const payloadKeys = useMemo(() => {
    const keys = new Set<string>();

    rows.forEach((row) => {
      if (row.payload && typeof row.payload === "object") {
        Object.keys(row.payload).forEach((key) => keys.add(key));
      }
    });

    return Array.from(keys);
  }, [rows]);

  /* ---------------------------------------
   * Render states
   * ------------------------------------- */
  if (loading) return <div id={id}>Loading audit logs…</div>;
  if (error) return <div id={id}>{error}</div>;

  /* ---------------------------------------
   * Render UI
   * ------------------------------------- */
  return (
    <div id={id} style={styles} className="audit-logs-wrapper">
      <h3>{title}</h3>

      {/* Toolbar */}
        <div className="audit-toolbar">
  <button
    onClick={() =>
      window.open(`${backendBase}/audit/logs/download?format=csv`, "_blank")
    }
  >
    Download CSV
  </button>

  <button
    onClick={() =>
      window.open(`${backendBase}/audit/logs/download?format=txt`, "_blank")
    }
  >
    Download TXT
  </button>

  <select value={limit} onChange={(e) => setLimit(Number(e.target.value))}>
    <option value={25}>25 rows</option>
    <option value={50}>50 rows</option>
    <option value={100}>100 rows</option>
  </select>
</div>

      {/* Table */}
      <div className="audit-table-container">
        <table className="audit-logs-table">
          <thead>
            <tr>
              <th>TX ID</th>
              <th>ACTION</th>
              <th>ENTITY</th>

              {payloadKeys.map((key) => (
                <th key={key}>
                  {(payloadLabelMap[key] ?? key).toUpperCase()}
                </th>
              ))}

              <th>CREATED AT</th>
            </tr>
          </thead>

          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                <td>{row.tx_id}</td>
                <td>{row.action}</td>
                <td>{row.entity}</td>

                {payloadKeys.map((key) => (
                  <td key={key}>
                    {row.payload?.[key] !== undefined
                      ? String(row.payload[key])
                      : ""}
                  </td>
                ))}

                <td>{resolveCreatedAt(row)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="audit-pagination">
        <button
          disabled={offset === 0}
          onClick={() => setOffset(Math.max(0, offset - limit))}
        >
          Previous
        </button>

        <span>
          Showing {offset + 1} – {offset + rows.length}
        </span>

        <button
          disabled={rows.length < limit}
          onClick={() => setOffset(offset + limit)}
        >
          Next
        </button>
      </div>
    </div>
  );
};
