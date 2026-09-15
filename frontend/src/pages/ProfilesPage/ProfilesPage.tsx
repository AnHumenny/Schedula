import React from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { profilesApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  PageHeader,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Profile } from "../../shared/types";

export const ProfilesPage: React.FC = () => {
  const qc = useQueryClient();
  const form = useCrudModal({
    name: "",
    description: "",
    is_active: true,
  });

  const query = useQuery({
    queryKey: ["profiles"],
    queryFn: () => profilesApi.list(),
  });

  const createMut = useMutation({
    mutationFn: profilesApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["profiles"] });
      form.close();
    },
  });

  const updateMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      profilesApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["profiles"] });
      form.close();
    },
  });

  const removeMut = useMutation({
    mutationFn: profilesApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["profiles"] }),
  });

  const saving = createMut.isPending || updateMut.isPending;
  const error = (createMut.error ?? updateMut.error) as Error | null;

  const openEdit = (p: Profile) =>
    form.openEdit(p.id, {
      name: p.name,
      description: p.description ?? "",
      is_active: p.is_active,
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
      <PageHeader title="Профили">
        <Button variant="primary" onClick={form.openCreate}>
          + Добавить
        </Button>
      </PageHeader>

      {query.isLoading && <p className="muted">Загрузка…</p>}
      {query.isError && (
        <p className="error">Ошибка: {(query.error as Error).message}</p>
      )}

      {query.data && (
        <Table<Profile>
          data={query.data}
          rowKey={(p) => p.id}
          columns={[
            { key: "id", title: "ID" },
            { key: "name", title: "Название" },
            { key: "description", title: "Описание" },
            {
              key: "is_active",
              title: "Активен",
              render: (p) => (p.is_active ? "да" : "нет"),
            },
            {
              key: "actions",
              title: "",
              render: (p) => (
                <div style={{ display: "flex", gap: 6 }}>
                  <Button onClick={() => openEdit(p)}>Изменить</Button>
                  <Button
                    variant="danger"
                    onClick={() => {
                      if (confirm(`Удалить профиль «${p.name}»?`)) {
                        removeMut.mutate(p.id);
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
          form.editingId == null ? "Новый профиль" : "Редактирование профиля"
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
            <span style={{ fontSize: 13 }}>Активен</span>
          </label>
        )}
      </FormModal>
    </div>
  );
};