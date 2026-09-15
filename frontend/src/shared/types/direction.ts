import type { ID } from "./common";

export interface Direction {
  id: ID;
  name: string;
  academic_year: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DirectionCreate {
  name: string;
  academic_year: string;
  description?: string | null;
}