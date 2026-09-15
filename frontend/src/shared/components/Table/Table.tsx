import React from "react";
import styles from "./Table.module.css";

interface Column<T> {
  key: string;
  title: string;
  render?: (row: T) => React.ReactNode;
}

interface Props<T> {
  columns: Column<T>[];
  data: T[];
  rowKey: (row: T) => string | number;
  emptyText?: string;
}

export function Table<T>({ columns, data, rowKey, emptyText = "Нет данных" }: Props<T>) {
  return (
    <table className={styles.table}>
      <thead>
        <tr>
          {columns.map((c) => <th key={c.key}>{c.title}</th>)}
        </tr>
      </thead>
      <tbody>
        {data.length === 0 && (
          <tr><td colSpan={columns.length} className="muted">{emptyText}</td></tr>
        )}
        {data.map((row) => (
          <tr key={rowKey(row)}>
            {columns.map((c) => (
              <td key={c.key}>
                {c.render ? c.render(row) : String((row as any)[c.key] ?? "")}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}