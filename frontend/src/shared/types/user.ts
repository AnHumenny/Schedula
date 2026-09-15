import type { ID } from "./common";

export type UserRole = "ADMIN" | "USER";

export interface User {
  id: ID;
  email: string;
  username: string;
  role: UserRole;
  is_active: boolean;
  group_id: ID | null;
  profile_id: ID | null;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
  role?: UserRole;
  group_id?: ID | null;
  profile_id?: ID | null;
}

export interface UserUpdate {
  email?: string;
  username?: string;
  role?: UserRole;
  is_active?: boolean;
  group_id?: ID | null;
  profile_id?: ID | null;
}