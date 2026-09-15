import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  scheduleApi,
  teachersApi,
  disciplinesApi,
  roomsApi,
  buildingsApi,
  groupsApi,
} from "../../../shared/api";
import {
  Button,
  CheckboxGroup,
  FormModal,
  Input,
  Select,
} from "../../../shared/components";
import type { LessonType, LessonStatus } from "../../../shared/types";

const LESSON_TYPES: LessonType[] = [
  "LECTURE",
  "PRACTICE",
  "LAB",
  "SEMINAR",
  "EXAM",
  "CONSULTATION",
];

const LESSON_STATUSES: LessonStatus[] = [
  "PLANNED",
  "CANCELLED",
  "RESCHEDULED",
];

const LESSON_TYPE_LABELS: Record<LessonType, string> = {
  LECTURE: "Лекция",
  PRACTICE: "ПЗ",
  LAB: "Лабораторная",
  SEMINAR: "Семинар",
  EXAM: "Экзамен",
  CONSULTATION: "Консультация",
};

const LESSON_STATUS_LABELS: Record<LessonStatus, string> = {
  PLANNED: "Запланировано",
  CANCELLED: "Отменено",
  RESCHEDULED: "Перенесено",
};

const toLocalInput = (iso: string | null | undefined): string => {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return "";
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(
    d.getDate()
  )}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
};

const fromLocalInput = (local: string): string => {
  if (!local) return "";
  return local.length === 16 ? `${local}:00` : local;
};

export const ScheduleItemEditPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const itemId = Number(id);
  const navigate = useNavigate();
  const qc = useQueryClient();

  const itemQuery = useQuery({
    queryKey: ["schedule", "item", itemId],
    queryFn: () => scheduleApi.get(itemId),
    enabled: Number.isFinite(itemId),
  });

  const teachers = useQuery({
    queryKey: ["teachers"],
    queryFn: () => teachersApi.list(),
  });
  const disciplines = useQuery({
    queryKey: ["disciplines"],
    queryFn: () => disciplinesApi.list(),
  });
  const rooms = useQuery({
    queryKey: ["rooms"],
    queryFn: () => roomsApi.list(),
  });
  const buildings = useQuery({
    queryKey: ["buildings"],
    queryFn: () => buildingsApi.list(),
  });
  const groups = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
  });

  const buildingById = useMemo(
    () => new Map((buildings.data ?? []).map((b) => [b.id, b.name])),
    [buildings.data]
  );

  const roomLabel = (roomId: number) => {
    const room = (rooms.data ?? []).find((r) => r.id === roomId);
    if (!room) return `#${roomId}`;
    const b = buildingById.get(room.building_id);
    return b ? `${b} · ${room.number}` : room.number;
  };

  const [startLocal, setStartLocal] = useState("");
  const [endLocal, setEndLocal] = useState("");
  const [disciplineId, setDisciplineId] = useState("");
  const [teacherId, setTeacherId] = useState("");
  const [roomId, setRoomId] = useState("");
  const [groupIds, setGroupIds] = useState<number[]>([]);
  const [lessonType, setLessonType] = useState<LessonType>("LECTURE");
  const [status, setStatus] = useState<LessonStatus>("PLANNED");
  const [description, setDescription] = useState("");

  useEffect(() => {
    const item = itemQuery.data;
    if (!item) return;

    setStartLocal(toLocalInput(item.start_datetime));
    setEndLocal(toLocalInput(item.end_datetime));
    setDisciplineId(String(item.discipline_id));
    setTeacherId(String(item.teacher_id));
    setRoomId(String(item.room_id));
    setGroupIds(item.group_ids ?? []);
    setLessonType(item.lesson_type);
    setStatus(item.status);
    setDescription(item.description ?? "");
  }, [itemQuery.data]);

  const updateMut = useMutation({
    mutationFn: (data: any) => scheduleApi.update(itemId, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["schedule"] });
      navigate("/schedule/calendar/admin/");
    },
  });

  const removeMut = useMutation({
    mutationFn: () => scheduleApi.remove(itemId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["schedule"] });
      navigate("/schedule/calendar/admin/");
    },
  });

  const saving = updateMut.isPending || removeMut.isPending;
  const error = (updateMut.error ?? removeMut.error) as Error | null;

  const close = () => navigate("/schedule/calendar/admin/");

  const handleSubmit = () => {
    updateMut.mutate({
      start_datetime: fromLocalInput(startLocal),
      end_datetime: fromLocalInput(endLocal),
      discipline_id: Number(disciplineId),
      teacher_id: Number(teacherId),
      room_id: Number(roomId),
      group_ids: groupIds,
      lesson_type: lessonType,
      status,
      description: description || null,
    });
  };

  const handleDelete = () => {
    if (!confirm("Удалить это занятие?")) return;
    removeMut.mutate();
  };

  if (itemQuery.isLoading) {
    return (
      <div className="page">
        <p className="muted">Загрузка…</p>
      </div>
    );
  }

  if (itemQuery.isError || !itemQuery.data) {
    return (
      <div className="page">
        <p className="error">
          Не удалось загрузить занятие:{" "}
          {(itemQuery.error as Error)?.message ?? "не найдено"}
        </p>
      </div>
    );
  }

  return (
    <div className="page">
      <div
        style={{
          display: "flex",
          gap: 8,
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
        }}
      >
        <h1 className="page__title" style={{ margin: 0 }}>
          Редактирование занятия
        </h1>
        <Button onClick={close}>← К календарю</Button>
      </div>

      <FormModal
        open={true}
        title="Редактирование занятия"
        onClose={close}
        onSubmit={handleSubmit}
        saving={saving}
        error={error}
        submitLabel="Сохранить"
      >
        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ flex: 1 }}>
            <Input
              label="Начало"
              type="datetime-local"
              value={startLocal}
              onChange={(e) => setStartLocal(e.target.value)}
            />
          </div>
          <div style={{ flex: 1 }}>
            <Input
              label="Конец"
              type="datetime-local"
              value={endLocal}
              onChange={(e) => setEndLocal(e.target.value)}
            />
          </div>
        </div>

        <Select
          label="Дисциплина"
          value={disciplineId}
          onChange={setDisciplineId}
          placeholder="— выберите дисциплину —"
          options={(disciplines.data ?? []).map((d) => ({
            value: d.id,
            label: d.name,
          }))}
        />

        <Select
          label="Преподаватель"
          value={teacherId}
          onChange={setTeacherId}
          placeholder="— выберите преподавателя —"
          options={(teachers.data ?? []).map((t) => ({
            value: t.id,
            label: t.fullname,
          }))}
        />

        <Select
          label="Аудитория"
          value={roomId}
          onChange={setRoomId}
          placeholder="— выберите аудиторию —"
          options={(rooms.data ?? []).map((r) => ({
            value: r.id,
            label: roomLabel(r.id),
          }))}
        />

        <CheckboxGroup
          label="Группы"
          values={groupIds}
          onChange={setGroupIds}
          options={(groups.data ?? []).map((g) => ({
            value: g.id,
            label: g.name,
          }))}
          emptyText="Нет групп"
        />

        <div style={{ display: "flex", gap: 12 }}>
          <div style={{ flex: 1 }}>
            <Select
              label="Тип занятия"
              value={lessonType}
              onChange={(v) => setLessonType(v as LessonType)}
              options={LESSON_TYPES.map((t) => ({
                value: t,
                label: LESSON_TYPE_LABELS[t],
              }))}
            />
          </div>
          <div style={{ flex: 1 }}>
            <Select
              label="Статус"
              value={status}
              onChange={(v) => setStatus(v as LessonStatus)}
              options={LESSON_STATUSES.map((s) => ({
                value: s,
                label: LESSON_STATUS_LABELS[s],
              }))}
            />
          </div>
        </div>

        <Input
          label="Комментарий"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <div style={{ display: "flex", justifyContent: "flex-start" }}>
          <Button
            type="button"
            variant="danger"
            onClick={handleDelete}
            disabled={removeMut.isPending}
          >
            {removeMut.isPending ? "Удаление…" : "Удалить занятие"}
          </Button>
        </div>
      </FormModal>
    </div>
  );
};