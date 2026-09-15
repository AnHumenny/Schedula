import React from "react";
import { ScheduleCalendarAdmin } from "../../../components/calendar/ScheduleCalendarAdmin";
import "./ScheduleCalendarAdminPage.css";

export const ScheduleCalendarAdminPage: React.FC = () => (
  <div className="calendar-page">
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        marginBottom: 12,
      }}
    >
    </div>
    <ScheduleCalendarAdmin />
  </div>
);