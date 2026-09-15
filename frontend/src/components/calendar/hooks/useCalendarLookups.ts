import { useCallback, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  groupsApi,
  teachersApi,
  disciplinesApi,
  roomsApi,
  buildingsApi,
} from "../../../shared/api";

export function useCalendarLookups() {
  const groups = useQuery({
    queryKey: ["groups"],
    queryFn: () => groupsApi.list(),
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

  const disciplineById = useMemo(
    () => new Map((disciplines.data ?? []).map((d) => [d.id, d.name])),
    [disciplines.data]
  );
  const teacherById = useMemo(
    () => new Map((teachers.data ?? []).map((t) => [t.id, t.fullname])),
    [teachers.data]
  );
  const groupById = useMemo(
    () => new Map((groups.data ?? []).map((g) => [g.id, g.name])),
    [groups.data]
  );
  const buildingById = useMemo(
    () => new Map((buildings.data ?? []).map((b) => [b.id, b.name])),
    [buildings.data]
  );

  const roomLabel = useCallback(
    (roomId: number) => {
      const room = (rooms.data ?? []).find((r) => r.id === roomId);
      if (!room) return `ауд. #${roomId}`;
      const b = buildingById.get(room.building_id);
      return b ? `${b}, ${room.number}` : room.number;
    },
    [rooms.data, buildingById]
  );

  return {
    groups,
    teachers,
    disciplines,
    rooms,
    buildings,
    disciplineById,
    teacherById,
    groupById,
    buildingById,
    roomLabel,
  };
}