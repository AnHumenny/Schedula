import type { View } from "react-big-calendar";

const toLocalIso = (d: Date): string => {
  const pad = (n: number) => String(n).padStart(2, "0");
  return (
    `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
    `T${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
  );
};

export const getCalendarRange = (
  centerDate: Date,
  view: View = "month"
): { start: string; end: string } => {
  const y = centerDate.getFullYear();
  const m = centerDate.getMonth();
  const d = centerDate.getDate();

  if (view === "day" || view === "agenda") {
    const start = new Date(y, m, d, 0, 0, 0, 0);
    const end = new Date(y, m, d, 23, 59, 59, 999);
    return { start: toLocalIso(start), end: toLocalIso(end) };
  }

  if (view === "week") {
    const start = new Date(y, m, d);
    start.setDate(start.getDate() - 6);
    start.setHours(0, 0, 0, 0);

    const end = new Date(y, m, d);
    end.setDate(end.getDate() + 6);
    end.setHours(23, 59, 59, 999);

    return { start: toLocalIso(start), end: toLocalIso(end) };
  }

  const start = new Date(y, m, 1);
  start.setDate(start.getDate() - 6);
  start.setHours(0, 0, 0, 0);

  const end = new Date(y, m + 1, 0);
  end.setDate(end.getDate() + 6);
  end.setHours(23, 59, 59, 999);

  return { start: toLocalIso(start), end: toLocalIso(end) };
};