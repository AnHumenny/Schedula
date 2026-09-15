import { useQuery } from "@tanstack/react-query";
import {
  teachersApi,
  disciplinesApi,
  roomsApi,
  buildingsApi,
  groupsApi,
  profilesApi,
} from "../../../shared/api";

export function useLookups() {
  const teachers = useQuery({ queryKey: ["teachers"],    queryFn: () => teachersApi.list() });
  const disciplines = useQuery({ queryKey: ["disciplines"], queryFn: () => disciplinesApi.list() });
  const rooms = useQuery({ queryKey: ["rooms"],          queryFn: () => roomsApi.list() });
  const buildings = useQuery({ queryKey: ["buildings"],  queryFn: () => buildingsApi.list() });
  const groups = useQuery({ queryKey: ["groups"],        queryFn: () => groupsApi.list() });
  const profiles = useQuery({ queryKey: ["profiles"],    queryFn: () => profilesApi.list() });

  const teacherById = new Map((teachers.data ?? []).map((t) => [t.id, t.fullname]));
  const disciplineById = new Map((disciplines.data ?? []).map((d) => [d.id, d.name]));
  const groupById = new Map((groups.data ?? []).map((g) => [g.id, g.name]));
  const profileById = new Map((profiles.data ?? []).map((p) => [p.id, p.name]));
  const buildingById = new Map((buildings.data ?? []).map((b) => [b.id, b.name]));

  const roomLabel = (roomId: number) => {
    const room = (rooms.data ?? []).find((r) => r.id === roomId);
    if (!room) return `ауд. #${roomId}`;
    const building = buildingById.get(room.building_id);
    return building ? `${building}, ${room.number}` : room.number;
  };

  return {
    teacherById,
    disciplineById,
    groupById,
    profileById,
    roomLabel,
    isLoading:
      teachers.isLoading ||
      disciplines.isLoading ||
      rooms.isLoading ||
      buildings.isLoading ||
      groups.isLoading ||
      profiles.isLoading,
  };
}