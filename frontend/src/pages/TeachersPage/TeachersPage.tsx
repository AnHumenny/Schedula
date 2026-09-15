import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { teachersApi, disciplinesApi } from "../../shared/api";
import {
  Button,
  CheckboxGroup,
  FormModal,
  Input,
  PageHeader,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Teacher } from "../../shared/types";

export const TeachersPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    fullname: "",
    description: "",
    discipline_ids: [] as number[],
    is_active: true,
  });

  const teachersQuery = useQuery({
    queryKey: ["teachers"],
    queryFn: () => teachersApi.list(),
  });
  const disciplinesQuery = useQuery({
    queryKey: ["disciplines"],
    queryFn: () => disciplinesApi.list(),
  });

  const disciplineById = new Map(
    (disciplinesQuery.data ?? []).map((d) => [d.id, d.name])
  );

  const createMut = useMutation({
    mutationFn: teachersApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["teachers"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      teachersApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["teachers"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: teachersApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["teachers"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (t: Teacher) =>
    form.openEdit(t.id, {
      fullname: t.fullname,
      description: t.description ?? "",
      discipline_ids: t.discipline_ids ?? [],
      is_active: t.is_active,
    });

  const handleSubmit = () => {
    const base = {
      fullname: form.values.fullname,
      description: form.values.description || null,
      discipline_ids: form.values.discipline_ids,
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
      <PageHeader title="Преподаватели">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {teachersQuery.isLoading && <p className="muted">Загрузка…</p>}
      {teachersQuery.isError && (
        <p className="error">
          Ошибка: {(teachersQuery.error as Error).message}
        </p>
      )}

      {teachersQuery.data && (
        <Table<Teacher>
          data={teachersQuery.data}
          rowKey={(t) => t.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "fullname", title: "ФИО" },
            {
              key: "disciplines",
              title: "Дисциплины",
              render: (t) =>
                t.discipline_ids.length === 0
                  ? "—"
                  : t.discipline_ids
                      .map((id) => disciplineById.get(id) ?? `#${id}`)
                      .join(", "),
            },
            { key: "description", title: "Описание" },
            {
              key: "is_active",
              title: "Активен",
              render: (t) => (t.is_active ? "да" : "нет"),
            },
            {
              key: "actions",
              title: "",
              render: (t) => (
                <div style={{ display: "flex", gap: 6 }}>
                  <Button onClick={() => openEdit(t)}>Изменить</Button>
                  <Button
                    variant="danger"
                    onClick={() => {
                      if (confirm(`Удалить «${t.fullname}»?`)) {
                        removeMut.mutate(t.id);
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
            ? "Новый преподаватель"
            : "Редактирование преподавателя"
        }
        onClose={form.close}
        onSubmit={handleSubmit}
        saving={saving}
        error={error}
      >
        <Input
          label="ФИО"
          value={form.values.fullname}
          onChange={(e) => form.setField("fullname", e.target.value)}
        />
        <Input
          label="Описание"
          value={form.values.description}
          onChange={(e) => form.setField("description", e.target.value)}
        />

        <CheckboxGroup
          label="Дисциплины"
          values={form.values.discipline_ids}
          onChange={(v) => form.setField("discipline_ids", v)}
          options={(disciplinesQuery.data ?? []).map((d) => ({
            value: d.id,
            label: d.name,
          }))}
          emptyText="Нет дисциплин"
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