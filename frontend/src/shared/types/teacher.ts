import type { ID } from "./common";

export interface Teacher {
  id: ID;
  fullname: string;
  description: string | null;
  is_active: boolean;
  discipline_ids: ID[];
  created_at: string;
  updated_at: string;
}

export interface TeacherCreate {
  fullname: string;
  description?: string | null;
  discipline_ids?: ID[];
}