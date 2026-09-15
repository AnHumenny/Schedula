import type { ID } from "./common";

export interface Discipline {
  id: ID;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DisciplineCreate {
  name: string;
  description?: string | null;
}