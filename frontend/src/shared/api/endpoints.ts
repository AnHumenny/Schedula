import { api } from "./client";
import type {
  User, UserCreate, UserUpdate,
  Direction, DirectionCreate,
  Profile, ProfileCreate,
  Group, GroupCreate,
  Discipline, DisciplineCreate,
  Teacher, TeacherCreate,
  Building, Room, RoomCreate,
  ScheduleItem, ScheduleItemCreate,
  LoginRequest, LoginResponse,
} from "./types";

export const usersApi = {
  list: (limit = 50, offset = 0) =>
    api.get<User[]>("/users/", { params: { limit, offset } }).then((r) => r.data),
  get: (id: number) => api.get<User>(`/users/${id}`).then((r) => r.data),
  create: (data: UserCreate) =>
    api.post<User>("/users/", data).then((r) => r.data),
  update: (id: number, data: UserUpdate) =>
    api.patch<User>(`/users/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/users/${id}`),
};

export const directionsApi = {
  list: (onlyActive = false) =>
    api.get<Direction[]>("/directions/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Direction>(`/directions/${id}`).then((r) => r.data),
  create: (data: DirectionCreate) =>
    api.post<Direction>("/directions/", data).then((r) => r.data),
  update: (id: number, data: Partial<DirectionCreate> & { is_active?: boolean }) =>
    api.patch<Direction>(`/directions/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/directions/${id}`),
};

export const profilesApi = {
  list: (onlyActive = false) =>
    api.get<Profile[]>("/profiles/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Profile>(`/profiles/${id}`).then((r) => r.data),
  create: (data: ProfileCreate) =>
    api.post<Profile>("/profiles/", data).then((r) => r.data),
  update: (id: number, data: Partial<ProfileCreate> & { is_active?: boolean }) =>
    api.patch<Profile>(`/profiles/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/profiles/${id}`),
};

export const groupsApi = {
  list: (onlyActive = false) =>
    api.get<Group[]>("/groups/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Group>(`/groups/${id}`).then((r) => r.data),
  create: (data: GroupCreate) =>
    api.post<Group>("/groups/", data).then((r) => r.data),
  update: (id: number, data: Partial<GroupCreate> & { is_active?: boolean }) =>
    api.patch<Group>(`/groups/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/groups/${id}`),
};

export const disciplinesApi = {
  list: (onlyActive = false) =>
    api.get<Discipline[]>("/disciplines/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Discipline>(`/disciplines/${id}`).then((r) => r.data),
  create: (data: DisciplineCreate) =>
    api.post<Discipline>("/disciplines/", data).then((r) => r.data),
  update: (id: number, data: Partial<DisciplineCreate> & { is_active?: boolean }) =>
    api.patch<Discipline>(`/disciplines/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/disciplines/${id}`),
};

export const teachersApi = {
  list: (onlyActive = false) =>
    api.get<Teacher[]>("/teachers/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Teacher>(`/teachers/${id}`).then((r) => r.data),
  create: (data: TeacherCreate) =>
    api.post<Teacher>("/teachers/", data).then((r) => r.data),
  update: (id: number, data: Partial<TeacherCreate> & { is_active?: boolean }) =>
    api.patch<Teacher>(`/teachers/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/teachers/${id}`),
};

export const buildingsApi = {
  list: (onlyActive = false) =>
    api.get<Building[]>("/buildings/", { params: { only_active: onlyActive } })
      .then((r) => r.data),
  get: (id: number) => api.get<Building>(`/buildings/${id}`).then((r) => r.data),
  create: (data: Partial<Building>) =>
    api.post<Building>("/buildings/", data).then((r) => r.data),
  update: (id: number, data: Partial<Building>) =>
    api.patch<Building>(`/buildings/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/buildings/${id}`),
};

export const roomsApi = {
  list: (params: { building_id?: number; only_active?: boolean } = {}) =>
    api.get<Room[]>("/rooms/", { params }).then((r) => r.data),
  get: (id: number) => api.get<Room>(`/rooms/${id}`).then((r) => r.data),
  create: (data: RoomCreate) =>
    api.post<Room>("/rooms/", data).then((r) => r.data),
  update: (id: number, data: Partial<RoomCreate> & { is_active?: boolean }) =>
    api.patch<Room>(`/rooms/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/rooms/${id}`),
};

export const scheduleApi = {
  list: (params: { group_id?: number; teacher_id?: number; direction_id?: number; limit?: number; offset?: number;
      } = {}) => {
    if (params.group_id) {
      return api.get<ScheduleItem[]>(`/schedule/group/${params.group_id}`).then((r) => r.data);
    }
    if (params.teacher_id) {
      return api.get<ScheduleItem[]>(`/schedule/teacher/${params.teacher_id}`).then((r) => r.data);
    }
    return api.get<ScheduleItem[]>("/schedule/").then((r) => r.data);
  },

  range: (params: { start: string; end: string; group_id?: number; teacher_id?: number; direction_id?: number;
    }) =>
    api
      .get<ScheduleItem[]>("/schedule/range", { params })
      .then((r) => r.data),

  upcoming: (params: { days?: number; group_id?: number; teacher_id?: number; direction_id?: number; limit?: number;
    } = {}) =>
    api.get<ScheduleItem[]>("/schedule/upcoming", { params }).then((r) => r.data),

  get: (id: number) => api.get<ScheduleItem>(`/schedule/${id}`).then((r) => r.data),
  create: (data: ScheduleItemCreate) =>
    api.post<ScheduleItem>("/schedule/", data).then((r) => r.data),
  update: (id: number, data: Partial<ScheduleItemCreate>) =>
    api.patch<ScheduleItem>(`/schedule/${id}`, data).then((r) => r.data),
  remove: (id: number) => api.delete(`/schedule/${id}`),
};

export const authApi = {
  login: (data: LoginRequest) =>
    api.post<LoginResponse>("/auth/login", data).then((r) => r.data),

  me: () =>
    api.get<User>("/auth/me").then((r) => r.data),

  logout: () =>
    api.post("/auth/logout").then((r) => r.data),
};