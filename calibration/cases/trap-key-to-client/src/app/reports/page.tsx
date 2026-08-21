"use client";

import { useEffect, useState } from "react";
import { config } from "../../config";

type Row = { tenant: string; total: number };

export default function ReportsPage() {
  const [rows, setRows] = useState<Row[]>([]);

  useEffect(() => {
    fetch(`${config.apiUrl}/reports/cross-tenant`, {
      headers: { apikey: config.serviceRoleKey },
    })
      .then((r) => r.json())
      .then(setRows);
  }, []);

  return (
    <table>
      <tbody>
        {rows.map((r) => (
          <tr key={r.tenant}>
            <td>{r.tenant}</td>
            <td>{r.total}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
