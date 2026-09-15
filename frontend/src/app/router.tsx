import { createBrowserRouter, Navigate } from "react-router-dom";
import { Layout } from "./Layout";
import { RequireAuth } from "./guards/RequireAuth";

import { LoginPage } from "../pages/LoginPage/LoginPage";
import { DashboardPage } from "../pages/DashboardPage/DashboardPage";
import { SchedulePage } from "../pages/Schedule/SchedulePage/SchedulePage";
import { ScheduleCalendarPublicPage } from "../pages/Schedule/ScheduleCalendarPublicPage/ScheduleCalendarPublicPage";
import { ScheduleCalendarAdminPage } from "../pages/Schedule/ScheduleCalendarAdminPage/ScheduleCalendarAdminPage";
import { ScheduleItemCreatePage } from "../pages/Schedule/ScheduleItemCreatePage/ScheduleItemCreatePage";
import { TeachersPage } from "../pages/TeachersPage/TeachersPage";
import { ProfilesPage } from "../pages/ProfilesPage/ProfilesPage";
import { DisciplinesPage } from "../pages/DisciplinesPage/DisciplinesPage";
import { GroupsPage } from "../pages/GroupsPage/GroupsPage";
import { StudentsPage } from "../pages/StudentsPage/StudentsPage";
import { DirectionsPage } from "../pages/DirectionsPage/DirectionsPage";
import { LocationsPage } from "../pages/LocationsPage/LocationsPage";
import { ScheduleItemEditPage } from "../pages/Schedule/ScheduleItemEditPage/ScheduleItemEditPage";

export const router = createBrowserRouter([
  { path: "/schedule/calendar", element: <ScheduleCalendarPublicPage /> },

  { path: "/login", element: <LoginPage /> },

  {
    path: "/",
    element: (
      <RequireAuth requireRole="ADMIN">
        <Layout />
      </RequireAuth>
    ),
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: "dashboard",                element: <DashboardPage /> },
      { path: "schedule",                 element: <SchedulePage /> },
      { path: "schedule/calendar/admin",  element: <ScheduleCalendarAdminPage /> },
      { path: "schedule/create",          element: <ScheduleItemCreatePage /> },
      { path: "teachers",                 element: <TeachersPage /> },
      { path: "profiles",                 element: <ProfilesPage /> },
      { path: "groups",                   element: <GroupsPage /> },
      { path: "disciplines",              element: <DisciplinesPage /> },
      { path: "students",                 element: <StudentsPage /> },
      { path: "directions",               element: <DirectionsPage /> },
      { path: "locations",                element: <LocationsPage /> },
      { path: "schedule/:id/edit", element: <ScheduleItemEditPage /> },
    ],
  },

  { path: "*", element: <Navigate to="/login" replace /> },
]);