import axios from "axios";
import type {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

import { useAuthStore } from "../../features/auth/model/store";

const BASE_URL: string = import.meta.env.VITE_API_URL || "/api";

const LOGIN_PATH = "/login";
const PUBLIC_PATHS = ["/login", "/schedule/calendar"];

export const api: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

if (import.meta.env.DEV) {
  console.log("[api] baseURL =", BASE_URL);
}

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<{ detail?: string }>) => {
    const status = error.response?.status;

    if (
      status === 401 &&
      !PUBLIC_PATHS.includes(window.location.pathname)
    ) {
      useAuthStore.getState().logout();
      window.location.replace(LOGIN_PATH);
    }

    const detail =
      error.response?.data?.detail ?? error.message ?? "Unknown error";

    return Promise.reject(new Error(detail));
  }
);