import React from "react";
import { useNavigate } from "react-router-dom";
import { ScheduleCalendarPublic } from "../../../components/calendar/ScheduleCalendarPublic";
import { useAuthStore } from "../../../features/auth/model/store";
import { Button } from "../../../shared/components";
import styles from "./ScheduleCalendarPublicPage.module.css";

export const ScheduleCalendarPublicPage: React.FC = () => {
  const navigate = useNavigate();
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    logout();
    window.location.replace("/login");
  };

  return (
    <div className={styles.page}>
      <div className={styles.topbar}>
        <div className={styles.spacer} />

        {token ? (
          <div className={styles.userBox}>
            <span className={styles.username}>{user?.username}</span>
            <Button onClick={handleLogout}>Выйти</Button>
          </div>
        ) : (
          <Button onClick={() => navigate("/login")}>Войти</Button>
        )}
      </div>

      <ScheduleCalendarPublic />

      <footer className={styles.footer}>
        <a
          href="https://t.me/an_gumenniy"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.author}
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="currentColor"
            aria-hidden="true"
          >
            <path d="M21.94 4.6a1.75 1.75 0 0 0-1.87-.2L2.83 12.03a1.5 1.5 0 0 0 .13 2.76l3.98 1.24 1.5 4.9a1.5 1.5 0 0 0 2.5.66l2.13-2.05 4.16 3.05a1.5 1.5 0 0 0 2.34-.9L22.3 6.36a1.75 1.75 0 0 0-.36-1.76ZM9.9 15.1l-.4 3.06-1.06-3.48 9.06-6.44-7.6 6.86Zm2.1 1.02.24-1.7 5.06-4.58-5.3 6.28Z" />
          </svg>
          <span>@an_gumenniy</span>
        </a>
      </footer>
    </div>
  );
};