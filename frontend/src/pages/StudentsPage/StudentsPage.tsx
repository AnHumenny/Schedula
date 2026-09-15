import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { usersApi, groupsApi, profilesApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  PageHeader,
  Select,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import { USER_ROLE_LABELS } from "../../shared/constants";
import type { User, UserRole } from "../../shared/types";

const ROLES = ["USER", "ADMIN"] as const;

export const StudentsPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    email: "",
    username: "",
    password: "",
    role: "USER",
    group_id: "",
    profile_id: "",
    is_active: true,
  });

  const usersQuery = useQuery({
    queryKey: ["users"],
    queryFn: () => usersApi.list(),
  });
  const groupsQuery = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
  });
  const profilesQuery = useQuery({
    queryKey: ["profiles"],
    queryFn: () => profilesApi.list(),
  });

  const groupById = new Map(
    (groupsQuery.data ?? []).map((g) => [g.id, g.name])
  );
  const profileById = new Map(
    (profilesQuery.data ?? []).map((p) => [p.id, p.name])
  );

  const createMut = useMutation({
    mutationFn: usersApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["users"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      usersApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["users"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: usersApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (u: User) =>
    form.openEdit(u.id, {
      email: u.email,
      username: u.username,
      password: "",
      role: u.role,
      group_id: u.group_id != null ? String(u.group_id) : "",
      profile_id: u.profile_id != null ? String(u.profile_id) : "",
      is_active: u.is_active,
    });

   const handleSubmit = () => {
    const base: {
      email: string;
      username: string;
      role: UserRole;
      group_id: number | null;
      profile_id: number | null;
    } = {
      email: form.values.email,
      username: form.values.username,
      role: form.values.role as UserRole,
      group_id: form.values.group_id ? Number(form.values.group_id) : null,
      profile_id: form.values.profile_id
        ? Number(form.values.profile_id)
        : null,
    };

    if (form.editingId == null) {
      createMut.mutate({ ...base, password: form.values.password });
    } else {
      updateMut.mutate({
        id: form.editingId,
        data: { ...base, is_active: form.values.is_active },
      });
    }
  };

  return (
    <div className="page">
      <PageHeader title="Пользователи">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {usersQuery.isLoading && <p className="muted">Загрузка…</p>}
      {usersQuery.isError && (
        <p className="error">
          Ошибка: {(usersQuery.error as Error).message}
        </p>
      )}

      {usersQuery.data && (
        <Table<User>
          data={usersQuery.data}
          rowKey={(u) => u.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "username", title: "Username" },
            { key: "email", title: "Email" },
            {
              key: "role",
              title: "Роль",
              render: (u) => USER_ROLE_LABELS[u.role] ?? u.role,
            },
            {
              key: "group_id",
              title: "Группа",
              render: (u) =>
                u.group_id == null
                  ? "—"
                  : groupById.get(u.group_id) ?? `#${u.group_id}`,
            },
            {
              key: "profile_id",
              title: "Профиль",
              render: (u) =>
                u.profile_id == null
                  ? "—"
                  : profileById.get(u.profile_id) ?? `#${u.profile_id}`,
            },
            {
              key: "is_active",
              title: "Активен",
              render: (u) => (u.is_active ? "да" : "нет"),
            },
            {
              key: "actions",
              title: "",
              render: (u) => (
                <div style={{ display: "flex", gap: 6 }}>
                  <Button onClick={() => openEdit(u)}>Изменить</Button>
                  <Button
                    variant="danger"
                    disabled={u.username === "admin"}
                    onClick={() => {
                      if (confirm(`Удалить пользователя «${u.username}»?`)) {
                        removeMut.mutate(u.id);
                      }
                    }}
                  >
                    Удалить
                  </Button>
                </div>
              ),
            },
          ]}
        />
      )}

      <FormModal
        open={form.open}
        title={
          form.editingId == null
            ? "Новый пользователь"
            : "Редактирование пользователя"
        }
        onClose={form.close}
        onSubmit={handleSubmit}
        saving={saving}
        error={error}
      >
        <Input
          label="Email"
          type="email"
          value={form.values.email}
          onChange={(e) => form.setField("email", e.target.value)}
        />
        <Input
          label="Username"
          value={form.values.username}
          onChange={(e) => form.setField("username", e.target.value)}
        />

        {form.editingId == null && (
          <Input
            label="Пароль"
            type="password"
            value={form.values.password}
            onChange={(e) => form.setField("password", e.target.value)}
          />
        )}

        <Select
          label="Роль"
          value={form.values.role}
          onChange={(v) => form.setField("role", v)}
          options={ROLES.map((r) => ({
            value: r,
            label: USER_ROLE_LABELS[r] ?? r,
          }))}
        />

        <Select
          label="Группа"
          value={form.values.group_id}
          onChange={(v) => form.setField("group_id", v)}
          placeholder="— без группы —"
          options={(groupsQuery.data ?? []).map((g) => ({
            value: g.id,
            label: g.name,
          }))}
        />

        <Select
          label="Профиль"
          value={form.values.profile_id}
          onChange={(v) => form.setField("profile_id", v)}
          placeholder="— без профиля —"
          options={(profilesQuery.data ?? []).map((p) => ({
            value: p.id,
            label: p.name,
          }))}
        />

        {form.editingId != null && (
          <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <input
              type="checkbox"
              checked={form.values.is_active}
              onChange={(e) => form.setField("is_active", e.target.checked)}
            />
            <span style={{ fontSize: 13 }}>Активен</span>
          </label>
        )}
      </FormModal>
    </div>
  );
};