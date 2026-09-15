import type { ID } from "./common";

export interface Profile {
  id: ID;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProfileCreate {
  name: string;
  description?: string | null;
}