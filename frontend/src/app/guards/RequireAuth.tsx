import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../../features/auth/model/store";

interface Props {
  children: React.ReactNode;
  requireRole?: "ADMIN" | "USER";
}

export const RequireAuth: React.FC<Props> = ({ children, requireRole }) => {
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  if (requireRole && user?.role !== requireRole) {
    if (requireRole === "ADMIN" && user?.role === "USER") {
      return <Navigate to="/schedule/calendar" replace />;
    }
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};