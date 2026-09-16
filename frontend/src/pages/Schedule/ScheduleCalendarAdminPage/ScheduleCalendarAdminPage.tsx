import React from "react";
import { useNavigate } from "react-router-dom";
import { ScheduleCalendarAdmin } from "../../../components/calendar/ScheduleCalendarAdmin";
import { Button } from "../../../shared/components";
import "./ScheduleCalendarAdminPage.css";

export const ScheduleCalendarAdminPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="calendar-page">
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 12,
        }}
      >
        <h2 style={{ margin: 0, fontSize: 20 }}>Календарь занятий</h2>
        <Button onClick={() => navigate("/schedule/create")}>
          + Новое занятие
        </Button>
      </div>

      <ScheduleCalendarAdmin />
    </div>
  );
};