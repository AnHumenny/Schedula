import React from "react";
import type { Group, Teacher, Direction } from "../../../shared/types";
import styles from "./CalendarFilters.module.css";

interface Props {
  groups: Group[];
  teachers: Teacher[];
  directions: Direction[];
  filterGroupId: string;
  filterTeacherId: string;
  filterDirectionId: string;
  onChangeGroup: (v: string) => void;
  onChangeTeacher: (v: string) => void;
  onChangeDirection: (v: string) => void;
}

export const CalendarFilters: React.FC<Props> = ({
  groups,
  teachers,
  directions,
  filterGroupId,
  filterTeacherId,
  filterDirectionId,
  onChangeGroup,
  onChangeTeacher,
  onChangeDirection,
}) => {
  const hasFilter = filterGroupId || filterTeacherId || filterDirectionId;

  return (
    <div className={styles.wrap}>
      <label className={styles.field}>
        <span className={styles.label}>Направление</span>
        <select
          className={styles.select}
          value={filterDirectionId}
          onChange={(e) => onChangeDirection(e.target.value)}
        >
          <option value="">-----------------</option>
          {directions.map((d) => (
            <option key={d.id} value={d.id}>
              {d.name}
            </option>
          ))}
        </select>
      </label>

      <label className={styles.field}>
        <span className={styles.label}>Группа</span>
        <select
          className={styles.select}
          value={filterGroupId}
          onChange={(e) => {
            onChangeGroup(e.target.value);
            onChangeTeacher("");
          }}
        >
          <option value="">Все группы</option>
          {groups.map((g) => (
            <option key={g.id} value={g.id}>
              {g.name}
            </option>
          ))}
        </select>
      </label>

      <label className={styles.field}>
        <span className={styles.label}>Преподаватель</span>
        <select
          className={styles.select}
          value={filterTeacherId}
          onChange={(e) => {
            onChangeTeacher(e.target.value);
            onChangeGroup("");
          }}
        >
          <option value="">Все преподаватели</option>
          {teachers.map((t) => (
            <option key={t.id} value={t.id}>
              {t.fullname}
            </option>
          ))}
        </select>
      </label>

      {hasFilter && (
        <button
          className={styles.reset}
          onClick={() => {
            onChangeGroup("");
            onChangeTeacher("");
            onChangeDirection("");
          }}
        >
          Сбросить
        </button>
      )}
    </div>
  );
};