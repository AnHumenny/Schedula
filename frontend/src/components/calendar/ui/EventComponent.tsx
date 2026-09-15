import React from "react";
import { fmtTime } from "../../../shared/utils/date";
import type { CalendarEvent } from "../hooks/useCalendarEvents";
import styles from "./EventComponent.module.css";

interface Props {
  event: CalendarEvent;
  isMobile: boolean;
}

export const EventComponent: React.FC<Props> = ({ event, isMobile }) => {
  const r = event.resource;
  const timeStr = `${fmtTime(event.start.toISOString())}–${fmtTime(event.end.toISOString())}`;
  const title = `${r.disciplineName}\n${timeStr}\n${r.teacherName}\n${r.roomLabel}\nГруппы: ${r.groupNames}\n${r.lessonTypeLabel} · ${r.statusLabel}`;

  if (isMobile) {
    return (
      <div title={title} className={styles.mobile}>
        <div className={styles.title}>{r.disciplineName}</div>
        <div className={styles.time}>{timeStr}</div>
      </div>
    );
  }

  return (
    <div title={title} className={styles.desktop}>
      <div className={styles.title}>{r.disciplineName}</div>
      <div className={styles.sub}>
        {timeStr} · {r.teacherName}
      </div>
      <div className={styles.subMuted}>{r.roomLabel}</div>
    </div>
  );
};