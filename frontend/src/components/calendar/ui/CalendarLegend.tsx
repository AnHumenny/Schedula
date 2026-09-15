import React from "react";
import { colorForTeacher } from "../../../shared/utils/colors";
import styles from "./CalendarLegend.module.css";

interface Props {
  teachers: [number, string][];
  isMobile: boolean;
}

export const CalendarLegend: React.FC<Props> = ({ teachers, isMobile }) => (
  <div className={styles.legend}>
    {!isMobile && <span className={styles.title}>Преподаватели:</span>}
    {teachers.map(([id, name]) => (
      <div key={id} className={styles.item}>
        <span
          className={styles.dot}
          style={{
            background: colorForTeacher(id),
            width: isMobile ? 12 : 16,
            height: isMobile ? 12 : 16,
          }}
        />
        <span className={styles.name} style={{ fontSize: isMobile ? 11 : 13 }}>
          {name}
        </span>
      </div>
    ))}
  </div>
);