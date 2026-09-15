export interface Group {
  id: number;
  name: string;
  direction_id: number;
  profile_id: number | null;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface GroupCreate {
  name: string;
  direction_id: number;
  profile_id?: number | null;
  description?: string | null;
}