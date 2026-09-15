import React from "react";
import { RU_MONTHS, RU_VIEWS } from "../../../shared/constants/calendar";
import styles from "./CustomToolbar.module.css";

export const CustomToolbar: React.FC<any> = (toolbar) => {
  const goToBack = () => toolbar.onNavigate("PREV");
  const goToNext = () => toolbar.onNavigate("NEXT");
  const goToCurrent = () => toolbar.onNavigate("TODAY");

  const label = () => {
    const d = new Date(toolbar.date);
    if (toolbar.view === "week" || toolbar.view === "day") {
      return toolbar.label;
    }
    return `${RU_MONTHS[d.getMonth()]} ${d.getFullYear()}`;
  };

  return (
    <div className={styles.toolbar}>
      <button
        type="button"
        className={styles.btn}
        onClick={goToBack}
        title="Предыдущий"
        aria-label="Предыдущий"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>

      <button
        type="button"
        className={styles.btn}
        onClick={goToCurrent}
        title="Сегодня"
      >
        Сегодня
      </button>

      <button
        type="button"
        className={styles.btn}
        onClick={goToNext}
        title="Следующий"
        aria-label="Следующий"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>

      <span className={styles.label}>{label()}</span>

      <span className={styles.views}>
        {toolbar.views.map((v: string) => (
          <button
            key={v}
            type="button"
            className={`${styles.btn} ${toolbar.view === v ? styles.btnActive : ""}`}
            onClick={() => toolbar.onView(v)}
          >
            {RU_VIEWS[v] ?? v}
          </button>
        ))}
      </span>
    </div>
  );
};