import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { directionsApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  PageHeader,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Direction } from "../../shared/types";

export const DirectionsPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    name: "",
    academic_year: "",
    description: "",
    is_active: true,
  });

  const query = useQuery({
    queryKey: ["directions"],
    queryFn: () => directionsApi.list(),
  });

  const createMut = useMutation({
    mutationFn: directionsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["directions"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      directionsApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["directions"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: directionsApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["directions"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (d: Direction) =>
    form.openEdit(d.id, {
      name: d.name,
      academic_year: d.academic_year,
      description: d.description ?? "",
      is_active: d.is_active,
    });

  const handleSubmit = () => {
    const base = {
      name: form.values.name,
      academic_year: form.values.academic_year,
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
      <PageHeader title="Направления">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {query.isLoading && <p className="muted">Загрузка…</p>}
      {query.isError && (
        <p className="error">Ошибка: {(query.error as Error).message}</p>
      )}

      {query.data && (
        <Table<Direction>
          data={query.data}
          rowKey={(d) => d.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "name", title: "Название" },
            { key: "academic_year", title: "Учебный год" },
            { key: "description", title: "Описание" },
            {
              key: "is_active",
              title: "Активно",
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
                      if (confirm(`Удалить направление «${d.name}»?`)) {
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
            ? "Новое направление"
            : "Редактирование направления"
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
          label="Учебный год"
          value={form.values.academic_year}
          onChange={(e) => form.setField("academic_year", e.target.value)}
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
            <span style={{ fontSize: 13 }}>Активно</span>
          </label>
        )}
      </FormModal>
    </div>
  );
};