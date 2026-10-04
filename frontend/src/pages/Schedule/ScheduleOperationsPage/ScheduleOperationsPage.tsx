import React, { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  scheduleApi,
  groupsApi,
  directionsApi,
} from "../../../shared/api";
import {
  Button,
  Input,
  PageHeader,
  Select,
} from "../../../shared/components";

type Operation = "copy" | "delete";
type Target = "group" | "direction";

export const ScheduleOperationsPage: React.FC = () => {
  const qc = useQueryClient();

  const [operation, setOperation] = useState<Operation>("copy");
  const [target, setTarget] = useState<Target>("group");
  const [groupId, setGroupId] = useState("");
  const [directionId, setDirectionId] = useState("");
  const [sourceStart, setSourceStart] = useState("");
  const [sourceEnd, setSourceEnd] = useState("");
  const [startDate, setStartDate] = useState("");
  const [weeks, setWeeks] = useState("1");

  const groupsQuery = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
  });
  const directionsQuery = useQuery({
    queryKey: ["directions"],
    queryFn: () => directionsApi.list(),
  });

  const groups = groupsQuery.data ?? [];
  const directions = directionsQuery.data ?? [];

  const directionById = useMemo(
    () => new Map(directions.map((d) => [d.id, d.name])),
    [directions]
  );

  const mutation = useMutation({
    mutationFn: async () => {
      const weeksNum = Number(weeks);

      if (operation === "copy") {
        if (!sourceStart || !sourceEnd) {
          throw new Error("Укажите начало и конец исходного периода");
        }
        if (target === "group") {
          if (!groupId) throw new Error("Выберите группу");
          await scheduleApi.copyByGroup({
            source_start: sourceStart,
            source_end: sourceEnd,
            weeks_to_copy: weeksNum,
            group_id: Number(groupId),
          });
        } else {
          if (!directionId) throw new Error("Выберите направление");
          await scheduleApi.copyByDirection({
            source_start: sourceStart,
            source_end: sourceEnd,
            weeks_to_copy: weeksNum,
            direction_id: Number(directionId),
          });
        }
      } else {
        if (!startDate) throw new Error("Укажите дату начала");
        if (target === "group") {
          if (!groupId) throw new Error("Выберите группу");
          await scheduleApi.deleteByGroup({
            start_date: startDate,
            weeks_to_delete: weeksNum,
            group_id: Number(groupId),
          });
        } else {
          if (!directionId) throw new Error("Выберите направление");
          await scheduleApi.deleteByDirection({
            start_date: startDate,
            weeks_to_delete: weeksNum,
            direction_id: Number(directionId),
          });
        }
      }
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["schedule"] });
    },
  });

  const error = mutation.error as Error | null;

  const canSubmit = useMemo(() => {
    if (!weeks || Number(weeks) < 1) return false;
    if (target === "group" && !groupId) return false;
    if (target === "direction" && !directionId) return false;
    if (operation === "copy" && (!sourceStart || !sourceEnd)) return false;
    if (operation === "delete" && !startDate) return false;
    return true;
  }, [
    operation,
    target,
    groupId,
    directionId,
    sourceStart,
    sourceEnd,
    startDate,
    weeks,
  ]);

  return (
    <div className="page">
      <PageHeader title="Операции с расписанием" />

      <div
        className="card"
        style={{ display: "grid", gap: 12, maxWidth: 720 }}
      >
        <div style={{ display: "flex", gap: 16 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <input
              type="radio"
              name="operation"
              checked={operation === "copy"}
              onChange={() => setOperation("copy")}
            />
            <span>Копировать</span>
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <input
              type="radio"
              name="operation"
              checked={operation === "delete"}
              onChange={() => setOperation("delete")}
            />
            <span>Удалить</span>
          </label>
        </div>

        <div style={{ display: "flex", gap: 16 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <input
              type="radio"
              name="target"
              checked={target === "group"}
              onChange={() => setTarget("group")}
            />
            <span>По группе</span>
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <input
              type="radio"
              name="target"
              checked={target === "direction"}
              onChange={() => setTarget("direction")}
            />
            <span>По направлению</span>
          </label>
        </div>

        {target === "group" ? (
          <Select
            label="Группа"
            value={groupId}
            onChange={setGroupId}
            placeholder="— выберите группу —"
            options={groups.map((g) => {
              const dirName = directionById.get(g.direction_id);
              return {
                value: g.id,
                label: dirName ? `${g.name} (${dirName})` : g.name,
              };
            })}
          />
        ) : (
          <Select
            label="Направление"
            value={directionId}
            onChange={setDirectionId}
            placeholder="— выберите направление —"
            options={directions.map((d) => ({
              value: d.id,
              label: `${d.name} (${d.academic_year})`,
            }))}
          />
        )}

        {operation === "copy" ? (
          <>
            <Input
              label="Начало исходного периода"
              type="date"
              value={sourceStart}
              onChange={(e) => setSourceStart(e.target.value)}
            />
            <Input
              label="Конец исходного периода"
              type="date"
              value={sourceEnd}
              onChange={(e) => setSourceEnd(e.target.value)}
            />
            <Input
              label="Сколько недель копировать (макс. 52)"
              type="number"
              min={1}
              value={weeks}
              onChange={(e) => setWeeks(e.target.value)}
            />
          </>
        ) : (
          <>
            <Input
              label="Дата начала удаления"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
            <Input
              label="Сколько недель удалить"
              type="number"
              min={1}
              value={weeks}
              onChange={(e) => setWeeks(e.target.value)}
            />
          </>
        )}

        {error && <p className="error">Ошибка: {error.message}</p>}
        {mutation.isSuccess && (
          <p className="muted">
            Готово: операция «
            {operation === "copy" ? "копирование" : "удаление"}» выполнена.
          </p>
        )}

        <div style={{ display: "flex", gap: 8 }}>
          <Button
            variant="primary"
            disabled={!canSubmit || mutation.isPending}
            onClick={() => mutation.mutate()}
          >
            {mutation.isPending
              ? "Выполняется…"
              : operation === "copy"
              ? "Копировать"
              : "Удалить"}
          </Button>
        </div>
      </div>
    </div>
  );
};