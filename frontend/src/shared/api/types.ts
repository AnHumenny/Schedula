export type {
  User,
  UserCreate,
  UserUpdate,
  Direction,
  DirectionCreate,
  Profile,
  ProfileCreate,
  Group,
  GroupCreate,
  Discipline,
  DisciplineCreate,
  Teacher,
  TeacherCreate,
  Building,
  Room,
  RoomCreate,
  ScheduleItem,
  ScheduleItemCreate,
  LessonType,
  LessonStatus,
} from "../types";

export interface ApiError {
  detail: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
