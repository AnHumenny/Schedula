export type LessonType =
  | "LECTURE"
  | "PRACTICE"
  | "LAB"
  | "SEMINAR"
  | "EXAM"
  | "CONSULTATION";

export type LessonStatus = "PLANNED" | "CANCELLED" | "RESCHEDULED";

export interface ScheduleItem {
  id: number;
  group_ids: number[];
  teacher_id: number;
  discipline_id: number;
  room_id: number;
  start_datetime: string;
  end_datetime: string;
  lesson_type: LessonType;
  status: LessonStatus;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ScheduleItemCreate {
  group_ids: number[];
  teacher_id: number;
  discipline_id: number;
  room_id: number;
  start_datetime: string;
  end_datetime: string;
  lesson_type?: LessonType;
  status?: LessonStatus;
  description?: string | null;
}

export interface ScheduleItemUpdate {
  group_ids?: number[];
  teacher_id?: number;
  discipline_id?: number;
  room_id?: number;
  start_datetime?: string;
  end_datetime?: string;
  lesson_type?: LessonType;
  status?: LessonStatus;
  description?: string | null;
}
