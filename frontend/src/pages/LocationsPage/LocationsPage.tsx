import React, { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { buildingsApi, roomsApi } from "../../shared/api";
import {
  Button,
  FormModal,
  Input,
  Select,
  Table,
} from "../../shared/components";
import { useCrudModal } from "../../shared/hooks/useCrudModal";
import type { Building, Room } from "../../shared/types";

export const LocationsPage: React.FC = () => {
  const qc = useQueryClient();

  const [buildingsOpen, setBuildingsOpen] = useState(false);
  const [roomsOpen, setRoomsOpen] = useState(false);

  const bForm = useCrudModal({
    name: "",
    address: "",
    description: "",
    is_active: true,
  });

  const buildingsQuery = useQuery({
    queryKey: ["buildings"],
    queryFn: () => buildingsApi.list(),
  });

  const createBuildingMut = useMutation({
    mutationFn: buildingsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["buildings"] });
      bForm.close();
    },
  });

  const updateBuildingMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      buildingsApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["buildings"] });
      bForm.close();
    },
  });

  const removeBuildingMut = useMutation({
    mutationFn: buildingsApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["buildings"] }),
  });

  const bSaving = createBuildingMut.isPending || updateBuildingMut.isPending;
  const bError = (createBuildingMut.error ?? updateBuildingMut.error) as
    | Error
    | null;

  const openEditBuilding = (b: Building) =>
    bForm.openEdit(b.id, {
      name: b.name,
      address: b.address,
      description: b.description ?? "",
      is_active: b.is_active,
    });

  const handleBuildingSubmit = () => {
    const base = {
      name: bForm.values.name,
      address: bForm.values.address,
      description: bForm.values.description || null,
    };
    if (bForm.editingId == null) {
      createBuildingMut.mutate(base);
    } else {
      updateBuildingMut.mutate({
        id: bForm.editingId,
        data: { ...base, is_active: bForm.values.is_active },
      });
    }
  };

  const rForm = useCrudModal({
    building_id: "",
    number: "",
    description: "",
    is_active: true,
  });

  const roomsQuery = useQuery({
    queryKey: ["rooms"],
    queryFn: () => roomsApi.list(),
  });

  const buildingById = new Map(
    (buildingsQuery.data ?? []).map((b) => [b.id, b.name])
  );

  const createRoomMut = useMutation({
    mutationFn: roomsApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["rooms"] });
      rForm.close();
    },
  });

  const updateRoomMut = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      roomsApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["rooms"] });
      rForm.close();
    },
  });

  const removeRoomMut = useMutation({
    mutationFn: roomsApi.remove,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["rooms"] }),
  });

  const rSaving = createRoomMut.isPending || updateRoomMut.isPending;
  const rError = (createRoomMut.error ?? updateRoomMut.error) as
    | Error
    | null;

  const openEditRoom = (r: Room) =>
    rForm.openEdit(r.id, {
      building_id: String(r.building_id),
      number: r.number,
      description: r.description ?? "",
      is_active: r.is_active,
    });

  const handleRoomSubmit = () => {
    const base = {
      building_id: Number(rForm.values.building_id),
      number: rForm.values.number,
      description: rForm.values.description || null,
    };
    if (rForm.editingId == null) {
      createRoomMut.mutate(base);
    } else {
      updateRoomMut.mutate({
        id: rForm.editingId,
        data: { ...base, is_active: rForm.values.is_active },
      });
    }
  };

  return (
    <div className="page">
      <h1 className="page__title" style={{ marginBottom: 24 }}>
        Локации
      </h1>

      <div className="page__header">
        <h2
          style={{ fontSize: 18, margin: 0, cursor: "pointer" }}
          onClick={() => setBuildingsOpen((v) => !v)}
        >
          {buildingsOpen ? "▾" : "▸"} Корпуса
          {buildingsQuery.data && (
            <span
              className="muted"
              style={{ marginLeft: 8, fontSize: 14, fontWeight: 400 }}
            >
              ({buildingsQuery.data.length})
            </span>
          )}
        </h2>
        <div style={{ display: "flex", gap: 8 }}>
          <Button onClick={() => setBuildingsOpen((v) => !v)}>
            {buildingsOpen ? "Свернуть" : "Развернуть"}
          </Button>
          <Button variant="primary" onClick={bForm.openCreate}>
            + Добавить корпус
          </Button>
        </div>
      </div>

      {buildingsOpen && (
        <>
          {buildingsQuery.isLoading && <p className="muted">Загрузка…</p>}
          {buildingsQuery.isError && (
            <p className="error">
              Ошибка: {(buildingsQuery.error as Error).message}
            </p>
          )}
          {buildingsQuery.data && (
            <Table<Building>
              data={buildingsQuery.data}
              rowKey={(b) => b.id}
              columns={[
                { key: "id", title: "ID" },
                { key: "name", title: "Название" },
                { key: "address", title: "Адрес" },
                { key: "description", title: "Описание" },
                {
                  key: "is_active",
                  title: "Активен",
                  render: (b) => (b.is_active ? "да" : "нет"),
                },
                {
                  key: "actions",
                  title: "",
                  render: (b) => (
                    <div style={{ display: "flex", gap: 6 }}>
                      <Button onClick={() => openEditBuilding(b)}>
                        Изменить
                      </Button>
                      <Button
                        variant="danger"
                        onClick={() => {
                          if (confirm(`Удалить корпус «${b.name}»?`)) {
                            removeBuildingMut.mutate(b.id);
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
        </>
      )}

      <div className="page__header" style={{ marginTop: 40 }}>
        <h2
          style={{ fontSize: 18, margin: 0, cursor: "pointer" }}
          onClick={() => setRoomsOpen((v) => !v)}
        >
          {roomsOpen ? "▾" : "▸"} Аудитории
          {roomsQuery.data && (
            <span
              className="muted"
              style={{ marginLeft: 8, fontSize: 14, fontWeight: 400 }}
            >
              ({roomsQuery.data.length})
            </span>
          )}
        </h2>
        <div style={{ display: "flex", gap: 8 }}>
          <Button onClick={() => setRoomsOpen((v) => !v)}>
            {roomsOpen ? "Свернуть" : "Развернуть"}
          </Button>
          <Button variant="primary" onClick={rForm.openCreate}>
            + Добавить аудиторию
          </Button>
        </div>
      </div>

      {roomsOpen && (
        <>
          {roomsQuery.isLoading && <p className="muted">Загрузка…</p>}
          {roomsQuery.isError && (
            <p className="error">
              Ошибка: {(roomsQuery.error as Error).message}
            </p>
          )}
          {roomsQuery.data && (
            <Table<Room>
              data={roomsQuery.data}
              rowKey={(r) => r.id}
              columns={[
                { key: "id", title: "ID" },
                {
                  key: "building_id",
                  title: "Корпус",
                  render: (r) =>
                    buildingById.get(r.building_id) ?? `#${r.building_id}`,
                },
                { key: "number", title: "Номер" },
                { key: "description", title: "Описание" },
                {
                  key: "is_active",
                  title: "Активна",
                  render: (r) => (r.is_active ? "да" : "нет"),
                },
                {
                  key: "actions",
                  title: "",
                  render: (r) => (
                    <div style={{ display: "flex", gap: 6 }}>
                      <Button onClick={() => openEditRoom(r)}>Изменить</Button>
                      <Button
                        variant="danger"
                        onClick={() => {
                          if (confirm(`Удалить аудиторию «${r.number}»?`)) {
                            removeRoomMut.mutate(r.id);
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
        </>
      )}

      <FormModal
        open={bForm.open}
        title={bForm.editingId == null ? "Новый корпус" : "Редактирование корпуса"}
        onClose={bForm.close}
        onSubmit={handleBuildingSubmit}
        saving={bSaving}
        error={bError}
      >
        <Input
          label="Название"
          value={bForm.values.name}
          onChange={(e) => bForm.setField("name", e.target.value)}
        />
        <Input
          label="Адрес"
          value={bForm.values.address}
          onChange={(e) => bForm.setField("address", e.target.value)}
        />
        <Input
          label="Описание"
          value={bForm.values.description}
          onChange={(e) => bForm.setField("description", e.target.value)}
        />
        {bForm.editingId != null && (
          <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <input
              type="checkbox"
              checked={bForm.values.is_active}
              onChange={(e) => bForm.setField("is_active", e.target.checked)}
            />
            <span style={{ fontSize: 13 }}>Активен</span>
          </label>
        )}
      </FormModal>

      <FormModal
        open={rForm.open}
        title={
          rForm.editingId == null ? "Новая аудитория" : "Редактирование аудитории"
        }
        onClose={rForm.close}
        onSubmit={handleRoomSubmit}
        saving={rSaving}
        error={rError}
      >
        <Select
          label="Корпус"
          value={rForm.values.building_id}
          onChange={(v) => rForm.setField("building_id", v)}
          placeholder="— выберите корпус —"
          options={(buildingsQuery.data ?? []).map((b) => ({
            value: b.id,
            label: b.name,
          }))}
        />
        <Input
          label="Номер"
          value={rForm.values.number}
          onChange={(e) => rForm.setField("number", e.target.value)}
        />
        <Input
          label="Описание"
          value={rForm.values.description}
          onChange={(e) => rForm.setField("description", e.target.value)}
        />
        {rForm.editingId != null && (
          <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <input
              type="checkbox"
              checked={rForm.values.is_active}
              onChange={(e) => rForm.setField("is_active", e.target.checked)}
            />
            <span style={{ fontSize: 13 }}>Активна</span>
          </label>
        )}
      </FormModal>
    </div>
  );
};
