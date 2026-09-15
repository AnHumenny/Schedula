import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { disciplinesApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  PageHeader,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Discipline } from "../../shared/types";

export const DisciplinesPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    name: "",
    description: "",
    is_active: true,
  });

  const query = useQuery({
    queryKey: ["disciplines"],
    queryFn: () => disciplinesApi.list(),
  });

  const createMut = useMutation({
    mutationFn: disciplinesApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["disciplines"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      disciplinesApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["disciplines"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: disciplinesApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["disciplines"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (d: Discipline) =>
    form.openEdit(d.id, {
      name: d.name,
      description: d.description ?? "",
      is_active: d.is_active,
    });

  const handleSubmit = () => {
    const base = {
      name: form.values.name,
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
      <PageHeader title="Дисциплины">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {query.isLoading && <p className="muted">Загрузка…</p>}
      {query.isError && (
        <p className="error">Ошибка: {(query.error as Error).message}</p>
      )}

      {query.data && (
        <Table<Discipline>
          data={query.data}
          rowKey={(d) => d.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "name", title: "Название" },
            { key: "description", title: "Описание" },
            {
              key: "is_active",
              title: "Активна",
              render: (d) => (d.is_active ? "да" : "нет"),
            },
            {
              key: "actions",
              title: "",
              render: (d) => (
                <div style={{ display: "flex", gap: 6 }}>
                  <Button onClick={() => openEdit(d)}>Изменить</Button>
                  <Button
                    variant="danger"
                    onClick={() => {
                      if (confirm(`Удалить дисциплину «${d.name}»?`)) {
                        removeMut.mutate(d.id);
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
            ? "Новая дисциплина"
            : "Редактирование дисциплины"
        }
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