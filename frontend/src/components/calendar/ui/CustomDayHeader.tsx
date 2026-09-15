import React from "react";
import {
  RU_WEEKDAYS_SHORT,
  RU_MONTHS_GENITIVE,
} from "../../../shared/constants/calendar";
import styles from "./CustomDayHeader.module.css";

export const CustomDayHeader: React.FC<any> = ({ date }) => {
  const d = new Date(date);
  const weekday = RU_WEEKDAYS_SHORT[d.getDay()];
  const dayMonth = `${d.getDate()} ${RU_MONTHS_GENITIVE[d.getMonth()]}`;

  return (
    <div className={styles.header}>
      <span className={styles.weekday}>{weekday}</span>
      <span className={styles.dayMonth}>{dayMonth}</span>
    </div>
  );
};