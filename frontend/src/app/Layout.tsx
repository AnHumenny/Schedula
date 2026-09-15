import React from "react";
import { NavLink, Outlet } from "react-router-dom";
import { useAuthStore } from "../features/auth/model/store";
import "./Layout.css";

const NAV = [
  { to: "/dashboard",                label: "Дашборд" },
  { to: "/directions",               label: "Направления" },
  { to: "/schedule",                 label: "Расписание" },
  { to: "/schedule/calendar/admin/", label: "Календарь" },
  { to: "/teachers",                 label: "Преподаватели" },
  { to: "/groups",                   label: "Группы" },
  { to: "/profiles",                 label: "Профили" },
  { to: "/disciplines",              label: "Предметы" },
  { to: "/students",                 label: "Пользователи" },
  { to: "/locations",                label: "Локации" },
];

export const Layout: React.FC = () => {
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    logout();
    window.location.replace("/login");
  };

  return (
    <div className="layout">
      <aside className="layout__sidebar">
        <div className="layout__brand">Schedula</div>
        <nav className="layout__nav">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `layout__link${isActive ? " layout__link--active" : ""}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="layout__footer">
          {user && (
            <div className="layout__user">
              {user.username} · {user.role}
            </div>
          )}
          <button
            type="button"
            onClick={handleLogout}
            className="layout__logout"
          >
            Выйти
          </button>

          <a
            href="https://t.me/an_gumenniy"
            target="_blank"
            rel="noopener noreferrer"
            className="layout__author"
          >
            ✈ feedback: @an_gumenniy
          </a>
        </div>
      </aside>

      <main className="layout__content">
        <Outlet />
      </main>
    </div>
  );
};