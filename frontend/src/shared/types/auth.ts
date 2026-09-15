import type { ID } from "./common";
import type { UserRole } from "./user";

export interface AuthUser {
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

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
