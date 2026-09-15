import React from "react";
import styles from "./CalendarStats.module.css";

interface Props {
  total: number;
  planned: number;
  rescheduled: number;
  cancelled: number;
  isMobile: boolean;
  todayLabel?: string;
}

export const CalendarStats: React.FC<Props> = ({
  total,
  planned,
  rescheduled,
  cancelled,
  isMobile,
  todayLabel,
}) => (
  <div className={styles.stats} style={{ fontSize: isMobile ? 11 : 13 }}>
    <span>📊 Всего: {total}</span>
    <span>📌 Запланировано: {planned}</span>
    <span>⚠️ Перенесено: {rescheduled}</span>
    <span>❌ Отменено: {cancelled}</span>
    {!isMobile && todayLabel && <span>📅 {todayLabel}</span>}
  </div>
);