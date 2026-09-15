import React from "react";
import { fmtDate, fmtTime } from "../../../shared/utils/date";
import type { CalendarEvent } from "../hooks/useCalendarEvents";
import type { ScheduleItem } from "../../../shared/types";
import styles from "./EventDetailsModal.module.css";

interface Props {
  event: CalendarEvent;
  onClose: () => void;
  onEdit?: (item: ScheduleItem) => void;
  onDelete?: (item: ScheduleItem) => void;
}

const Row: React.FC<{ label: string; value: React.ReactNode }> = ({
  label,
  value,
}) => (
  <div className={styles.row}>
    <span className={styles.rowLabel}>{label}</span>
    <span className={styles.rowValue}>{value}</span>
  </div>
);

export const EventDetailsModal: React.FC<Props> = ({
  event,
  onClose,
  onEdit,
  onDelete,
}) => {
  const r = event.resource;
  const item = r.item;

  return (
    <div className={styles.backdrop} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <div>
            <h2 className={styles.title}>{r.disciplineName}</h2>
            <div className={styles.subtitle}>
              {r.lessonTypeLabel} · {r.statusLabel}
            </div>
          </div>
          <button
            className={styles.closeBtn}
            onClick={onClose}
            aria-label="Закрыть"
          >
            ✕
          </button>
        </div>

        <Row label="Дата" value={fmtDate(item.start_datetime)} />
        <Row
          label="Время"
          value={`${fmtTime(item.start_datetime)} – ${fmtTime(item.end_datetime)}`}
        />
        <Row label="Преподаватель" value={r.teacherName} />
        <Row label="Аудитория" value={r.roomLabel} />
        <Row label="Группы" value={r.groupNames} />
        {item.description && (
          <Row
            label="Комментарий"
            value={
              <span style={{ whiteSpace: "pre-wrap" }}>
                {item.description}
              </span>
            }
          />
        )}

        <div className={styles.actions}>
          {onDelete && (
            <button
              className={`${styles.btn} ${styles.btnDanger}`}
              onClick={() => onDelete(item)}
            >
              Удалить
            </button>
          )}
          {onEdit && (
            <button className={styles.btn} onClick={() => onEdit(item)}>
              Редактировать
            </button>
          )}
          <button
            className={`${styles.btn} ${styles.btnPrimary}`}
            onClick={onClose}
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  );
};