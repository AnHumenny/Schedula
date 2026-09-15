import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { groupsApi, directionsApi, profilesApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  PageHeader,
  Select,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Group } from "../../shared/types";

export const GroupsPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    name: "",
    direction_id: "",
    profile_id: "",
    description: "",
    is_active: true,
  });

  const groupsQuery = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
  });
  const directionsQuery = useQuery({
    queryKey: ["directions"],
    queryFn: () => directionsApi.list(),
  });
  const profilesQuery = useQuery({
    queryKey: ["profiles"],
    queryFn: () => profilesApi.list(),
  });

  const directionById = new Map(
    (directionsQuery.data ?? []).map((d) => [d.id, d.name])
  );
  const profileById = new Map(
    (profilesQuery.data ?? []).map((p) => [p.id, p.name])
  );

  const createMut = useMutation({
    mutationFn: groupsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["groups"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      groupsApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["groups"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: groupsApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["groups"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (g: Group) =>
    form.openEdit(g.id, {
      name: g.name,
      direction_id: String(g.direction_id),
      profile_id: g.profile_id != null ? String(g.profile_id) : "",
      description: g.description ?? "",
      is_active: g.is_active,
    });

  const handleSubmit = () => {
    const base = {
      name: form.values.name,
      direction_id: Number(form.values.direction_id),
      profile_id: form.values.profile_id
        ? Number(form.values.profile_id)
        : null,
      description: form.values.description || null,
    };
    if (form.editingId == null) {
      createMut.mutate(base);
    } else {
      updateMut.mutate({
        id: form.editingId,
        data: { ...base, is_active: form.values.is_active },
      });
    }
  };

  return (
    <div className="page">
      <PageHeader title="Группы">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {groupsQuery.isLoading && <p className="muted">Загрузка…</p>}
      {groupsQuery.isError && (
        <p className="error">
          Ошибка: {(groupsQuery.error as Error).message}
        </p>
      )}

      {groupsQuery.data && (
        <Table<Group>
          data={groupsQuery.data}
          rowKey={(g) => g.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "name", title: "Название" },
            {
              key: "direction_id",
              title: "Направление",
              render: (g) =>
                directionById.get(g.direction_id) ?? `#${g.direction_id}`,
            },
            {
              key: "profile_id",
              title: "Профиль",
              render: (g) =>
                g.profile_id == null
                  ? "—"
                  : profileById.get(g.profile_id) ?? `#${g.profile_id}`,
            },
            {
              key: "is_active",
              title: "Активна",
              render: (g) => (g.is_active ? "да" : "нет"),
            },
            {
              key: "actions",
              title: "",
              render: (g) => (
                <div style={{ display: "flex", gap: 6 }}>
                  <Button onClick={() => openEdit(g)}>Изменить</Button>
                  <Button
                    variant="danger"
                    onClick={() => {
                      if (confirm(`Удалить группу «${g.name}»?`)) {
                        removeMut.mutate(g.id);
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
        title={form.editingId == null ? "Новая группа" : "Редактирование группы"}
        onClose={form.close}
        onSubmit={handleSubmit}
        saving={saving}
        error={error}
      >
        <Input
          label="Название"
          value={form.values.name}
          onChange={(e) => form.setField("name", e.target.value)}
        />
        <Select
          label="Направление"
          value={form.values.direction_id}
          onChange={(v) => form.setField("direction_id", v)}
          placeholder="— выберите направление —"
          options={(directionsQuery.data ?? []).map((d) => ({
            value: d.id,
            label: `${d.name} (${d.academic_year})`,
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
        <Input
          label="Описание"
          value={form.values.description}
          onChange={(e) => form.setField("description", e.target.value)}
        />
        {form.editingId != null && (
          <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <input
              type="checkbox"
              checked={form.values.is_active}
              onChange={(e) => form.setField("is_active", e.target.checked)}
            />
            <span style={{ fontSize: 13 }}>Активна</span>
          </label>
        )}
      </FormModal>
    </div>
  );
};