import React from "react";
import type { Group, Teacher } from "../../../shared/types";
import styles from "./CalendarFilters.module.css";

interface Props {
  groups: Group[];
  teachers: Teacher[];
  filterGroupId: string;
  filterTeacherId: string;
  onChangeGroup: (v: string) => void;
  onChangeTeacher: (v: string) => void;
}

export const CalendarFilters: React.FC<Props> = ({
  groups,
  teachers,
  filterGroupId,
  filterTeacherId,
  onChangeGroup,
  onChangeTeacher,
}) => {
  const hasFilter = filterGroupId || filterTeacherId;

  return (
    <div className={styles.wrap}>
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
          }}
        >
          Сбросить
        </button>
      )}
    </div>
  );
};