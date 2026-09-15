import React, { useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
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

const toLocalInput = (iso: string | null): string => {
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

interface Props {
  onClose?: () => void;
}

export const ScheduleItemCreatePage: React.FC<Props> = ({ onClose }) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const qc = useQueryClient();

  const startParam = searchParams.get("start");

  const initialStart = useMemo(() => {
    const src = startParam ? new Date(startParam) : new Date();
    if (isNaN(src.getTime())) return new Date();
    return src;
  }, [startParam]);

  const initialEnd = useMemo(() => {
    const d = new Date(initialStart);
    d.setMinutes(d.getMinutes() + 90);
    return d;
  }, [initialStart]);

  const [startLocal, setStartLocal] = useState(
    toLocalInput(initialStart.toISOString())
  );
  const [endLocal, setEndLocal] = useState(
    toLocalInput(initialEnd.toISOString())
  );
  const [disciplineId, setDisciplineId] = useState<string>("");
  const [teacherId, setTeacherId] = useState<string>("");
  const [roomId, setRoomId] = useState<string>("");
  const [groupIds, setGroupIds] = useState<number[]>([]);
  const [lessonType, setLessonType] = useState<LessonType>("LECTURE");
  const [status, setStatus] = useState<LessonStatus>("PLANNED");
  const [description, setDescription] = useState("");

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

  const buildingById = new Map(
    (buildings.data ?? []).map((b) => [b.id, b.name])
  );

  const roomLabel = (id: number) => {
    const room = (rooms.data ?? []).find((r) => r.id === id);
    if (!room) return `#${id}`;
    const b = buildingById.get(room.building_id);
    return b ? `${b} · ${room.number}` : room.number;
  };

  const createMut = useMutation({
    mutationFn: scheduleApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["schedule"] });
      close();
    },
  });

  const saving = createMut.isPending;
  const error = createMut.error as Error | null;

  const close = () => {
    if (onClose) onClose();
    else navigate("/schedule/calendar/admin/");
  };

  const handleSubmit = () => {
    createMut.mutate({
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

  return (
    <FormModal
      open={true}
      title="Новое занятие"
      onClose={close}
      onSubmit={handleSubmit}
      saving={saving}
      error={error}
      submitLabel="Создать"
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
        placeholder="например: первая пара по расписанию"
      />
    </FormModal>
  );
};