import React, { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  usersApi,
  groupsApi,
  teachersApi,
  disciplinesApi,
  directionsApi,
  profilesApi,
  buildingsApi,
  roomsApi,
  scheduleApi,
} from "../../shared/api";
import {
  LESSON_TYPE_LABELS,
} from "../../shared/constants";

const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  });

const fmtDate = (iso: string) =>
  new Date(iso).toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "short",
  });

export const DashboardPage: React.FC = () => {
  const users = useQuery({ queryKey: ["users"], queryFn: () => usersApi.list() });
  const groups = useQuery({ queryKey: ["groups"], queryFn: () => groupsApi.list() });
  const teachers = useQuery({ queryKey: ["teachers"], queryFn: () => teachersApi.list() });
  const disciplines = useQuery({ queryKey: ["disciplines"], queryFn: () => disciplinesApi.list() });
  const directions = useQuery({ queryKey: ["directions"], queryFn: () => directionsApi.list() });
  const profiles = useQuery({ queryKey: ["profiles"], queryFn: () => profilesApi.list() });
  const buildings = useQuery({ queryKey: ["buildings"], queryFn: () => buildingsApi.list() });
  const rooms = useQuery({ queryKey: ["rooms"], queryFn: () => roomsApi.list() });

  const upcoming = useQuery({
    queryKey: ["schedule", "upcoming", { days: 1 }],
    queryFn: () => scheduleApi.upcoming({ days: 1 }),
  });

  const disciplineById = useMemo(
    () => new Map((disciplines.data ?? []).map((d) => [d.id, d.name])),
    [disciplines.data]
  );
  const teacherById = useMemo(
    () => new Map((teachers.data ?? []).map((t) => [t.id, t.fullname])),
    [teachers.data]
  );
  const groupById = useMemo(
    () => new Map((groups.data ?? []).map((g) => [g.id, g.name])),
    [groups.data]
  );
  const buildingById = useMemo(
    () => new Map((buildings.data ?? []).map((b) => [b.id, b.name])),
    [buildings.data]
  );
  const roomLabel = (roomId: number) => {
    const room = (rooms.data ?? []).find((r) => r.id === roomId);
    if (!room) return `#${roomId}`;
    const b = buildingById.get(room.building_id);
    return b ? `${b} · ${room.number}` : room.number;
  };

  const counters = [
    { label: "Направлений",    value: directions.data?.length },
    { label: "Групп",          value: groups.data?.length },
    { label: "Профилей",       value: profiles.data?.length },
    { label: "Дисциплин",      value: disciplines.data?.length },
    { label: "Преподавателей", value: teachers.data?.length },
    { label: "Пользователей",  value: users.data?.length },
    { label: "Корпусов",       value: buildings.data?.length },
    { label: "Аудиторий",      value: rooms.data?.length },
  ];

  const items = upcoming.data ?? [];

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Дашборд</h1>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
          gap: 16,
          marginBottom: 24,
        }}
      >
        {counters.map((c) => (
          <div key={c.label} className="card">
            <div style={{ fontSize: 28, fontWeight: 700 }}>
              {c.value ?? "—"}
            </div>
            <div className="muted" style={{ fontSize: 13 }}>
              {c.label}
            </div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3 style={{ fontSize: 16, fontWeight: 600, margin: "0 0 12px" }}>
          Ближайшие занятия (7 дней)
        </h3>

        {upcoming.isLoading && <p className="muted">Загрузка…</p>}
        {upcoming.isError && (
          <p className="error">
            Ошибка: {(upcoming.error as Error).message}
          </p>
        )}

        {!upcoming.isLoading && items.length === 0 && (
          <p className="muted">Занятий нет.</p>
        )}

        {items.map((item) => (
          <div
            key={item.id}
            style={{
              display: "flex",
              gap: 16,
              padding: "10px 0",
              borderBottom: "1px solid var(--color-border)",
            }}
          >
            <div
              style={{
                minWidth: 140,
                color: "var(--color-primary)",
                fontWeight: 600,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {fmtDate(item.start_datetime)},{" "}
              {fmtTime(item.start_datetime)}–{fmtTime(item.end_datetime)}
            </div>
            <div>
              <div style={{ fontWeight: 500 }}>
                {disciplineById.get(item.discipline_id) ??
                  `Дисциплина #${item.discipline_id}`}
              </div>
              <div className="muted" style={{ fontSize: 13 }}>
                {teacherById.get(item.teacher_id) ??
                  `Преподаватель #${item.teacher_id}`}{" "}
                · {roomLabel(item.room_id)} ·{" "}
                {LESSON_TYPE_LABELS[item.lesson_type] ?? item.lesson_type}
              </div>
              <div className="muted" style={{ fontSize: 12 }}>
                Группы:{" "}
                {item.group_ids
                  .map((id) => groupById.get(id) ?? `#${id}`)
                  .join(", ") || "—"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};