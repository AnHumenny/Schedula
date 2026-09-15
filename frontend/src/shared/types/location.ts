import type { ID } from "./common";

export interface Building {
  id: ID;
  name: string;
  address: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Room {
  id: ID;
  building_id: ID;
  number: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RoomCreate {
  building_id: ID;
  number: string;
  description?: string | null;
}