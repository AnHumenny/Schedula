import React, { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { scheduleApi, groupsApi, teachersApi } from "../../../shared/api";
import {
  LESSON_TYPE_LABELS,
  LESSON_STATUS_LABELS,
} from "../../../shared/constants";
import { Button, PageHeader, Select } from "../../../shared/components";
import { useLookups } from "./useLookups";
import styles from "./SchedulePage.module.css";
import type { ScheduleItem } from "../../../shared/types";

const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit",
  });

const fmtDay = (iso: string) =>
  new Date(iso).toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

const dayKey = (iso: string) => iso.slice(0, 10);

export const SchedulePage: React.FC = () => {
  const lookups = useLookups();
  const [groupId, setGroupId] = useState<string>("");
  const [teacherId, setTeacherId] = useState<string>("");

  const groupsQuery = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
  });
  const teachersQuery = useQuery({
    queryKey: ["teachers"],
    queryFn: () => teachersApi.list(),
  });

  const schedule = useQuery({
    queryKey: ["schedule", "upcoming", { groupId, teacherId }],
    queryFn: () =>
      scheduleApi.upcoming({
        days: 7,
        group_id: groupId ? Number(groupId) : undefined,
        teacher_id: teacherId ? Number(teacherId) : undefined,
        limit: 200,
      }),
  });

  const items: ScheduleItem[] = schedule.data ?? [];

  const sorted = useMemo(
    () =>
      items
        .slice()
        .sort((a, b) => a.start_datetime.localeCompare(b.start_datetime)),
    [items]
  );

  const grouped = useMemo(() => {
    const map = new Map<string, ScheduleItem[]>();
    sorted.forEach((i) => {
      const k = dayKey(i.start_datetime);
      if (!map.has(k)) map.set(k, []);
      map.get(k)!.push(i);
    });
    return Array.from(map.entries()).sort(([a], [b]) => a.localeCompare(b));
  }, [sorted]);

  const today = new Date().toLocaleDateString("ru-RU");
  const weekAhead = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    .toLocaleDateString("ru-RU");

  const hasFilter = groupId || teacherId;

  return (
    <div className="page">
      <PageHeader title="Расписание">
        <Link to="/schedule/calendar/admin/">
          <Button>Открыть календарь →</Button>
        </Link>
      </PageHeader>

      <div className={styles.filters}>
        <Select
          label="Группа"
          value={groupId}
          onChange={(v) => {
            setGroupId(v);
            setTeacherId("");
          }}
          placeholder="Все группы"
          options={(groupsQuery.data ?? []).map((g) => ({
            value: g.id,
            label: g.name,
          }))}
        />

        <Select
          label="Преподаватель"
          value={teacherId}
          onChange={(v) => {
            setTeacherId(v);
            setGroupId("");
          }}
          placeholder="Все преподаватели"
          options={(teachersQuery.data ?? []).map((t) => ({
            value: t.id,
            label: t.fullname,
          }))}
        />

        {hasFilter && (
          <Button
            className={styles.filter}
            onClick={() => {
              setGroupId("");
              setTeacherId("");
            }}
          >
            Сбросить
          </Button>
        )}
      </div>

      <p className="muted" style={{ marginBottom: 12, fontSize: 13 }}>
        Показаны занятия с {today} по {weekAhead}
      </p>

      {schedule.isLoading && <p className="muted">Загрузка…</p>}
      {schedule.isError && (
        <p className="error">Ошибка: {(schedule.error as Error).message}</p>
      )}

      {!schedule.isLoading && grouped.length === 0 && (
        <div className="card">
          <p className="muted">
            Занятий в ближайшие 7 дней по выбранным фильтрам нет.
          </p>
        </div>
      )}

      {grouped.map(([d, list]) => (
        <div key={d} className={styles.dayGroup}>
          <h2 className={styles.dayTitle}>{fmtDay(d)}</h2>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Время</th>
                <th>Дисциплина</th>
                <th>Преподаватель</th>
                <th>Группы</th>
                <th>Аудитория</th>
                <th>Тип</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody>
              {list.map((item) => (
                <tr key={item.id}>
                  <td className={styles.timeCell}>
                    {fmtTime(item.start_datetime)}–{fmtTime(item.end_datetime)}
                  </td>
                  <td>
                    {lookups.disciplineById.get(item.discipline_id) ??
                      `Дисциплина #${item.discipline_id}`}
                    {item.description && (
                      <div className="muted" style={{ fontSize: 12 }}>
                        {item.description}
                      </div>
                    )}
                  </td>
                  <td>
                    {lookups.teacherById.get(item.teacher_id) ??
                      `Преподаватель #${item.teacher_id}`}
                  </td>
                  <td>
                    {item.group_ids
                      .map((id) => lookups.groupById.get(id) ?? `#${id}`)
                      .join(", ") || "—"}
                  </td>
                  <td>{lookups.roomLabel(item.room_id)}</td>
                  <td>
                    <span className={`${styles.tag} ${styles.tagPrimary}`}>
                      {LESSON_TYPE_LABELS[item.lesson_type] ?? item.lesson_type}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`${styles.tag} ${
                        item.status === "CANCELLED"
                          ? styles.tagDanger
                          : item.status === "RESCHEDULED"
                          ? styles.tagWarning
                          : ""
                      }`}
                    >
                      {LESSON_STATUS_LABELS[item.status] ?? item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
};