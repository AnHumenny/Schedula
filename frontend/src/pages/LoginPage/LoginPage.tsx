import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { authApi } from "../../shared/api";
import { useAuthStore } from "../../features/auth/model/store";
import { Button, Input } from "../../shared/components";
import styles from "./LoginPage.module.css";

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const setToken = useAuthStore((s) => s.setToken);
  const setUser = useAuthStore((s) => s.setUser);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [fallbackError, setFallbackError] = useState<string | null>(null);

  const loginMut = useMutation({
    mutationFn: () => authApi.login({ username, password }),
    onSuccess: async (data) => {
      setToken(data.access_token);

      try {
        const me = await authApi.me();
        setUser(me);
        if (me.role === "ADMIN") navigate("/dashboard", { replace: true });
        else navigate("/schedule/calendar", { replace: true });
      } catch {
        navigate("/dashboard", { replace: true });
      }
    },
  });

  const handleDevLogin = (role: "ADMIN" | "USER") => {
    setFallbackError(null);
    if (!username || !password) {
      setFallbackError("Введите логин и пароль.");
      return;
    }
    setToken(`demo-${role.toLowerCase()}`);
    setUser({
      id: 0,
      email: `${username}@demo`,
      username,
      role,
      is_active: true,
      group_id: null,
      profile_id: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
    navigate(role === "ADMIN" ? "/dashboard" : "/schedule/calendar", {
      replace: true,
    });
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setFallbackError(null);
    loginMut.mutate();
  };

  return (
    <div className={styles.wrap}>
      <form className={styles.form} onSubmit={onSubmit}>
        <h1 className={styles.title}>Schedula</h1>
        <p className={styles.subtitle}>Вход в систему</p>

        <Input
          label="Логин"
          value={username}
          autoComplete="username"
          onChange={(e) => setUsername(e.target.value)}
        />
        <Input
          label="Пароль"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {loginMut.isError && (
          <div className={styles.error}>
            <div>
              Бэкенд авторизации пока не отвечает:{" "}
              <span className="muted">
                {(loginMut.error as Error).message}
              </span>
            </div>
            <div className={styles.errorActions}>
              <Button
                type="button"
                variant="primary"
                onClick={() => handleDevLogin("ADMIN")}
              >
                Войти как ADMIN
              </Button>
              <Button type="button" onClick={() => handleDevLogin("USER")}>
                Войти как USER
              </Button>
            </div>
          </div>
        )}

        {fallbackError && <p className={styles.fallbackError}>{fallbackError}</p>}

        <Button
          type="submit"
          variant="primary"
          disabled={!username || !password || loginMut.isPending}
        >
          {loginMut.isPending ? "Вход…" : "Войти"}
        </Button>
      </form>
    </div>
  );
};