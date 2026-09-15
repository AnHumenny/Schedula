export type ID = number;

export interface Paginated<T> {
  items: T[];
  total: number;
}

export interface PageParams {
  limit?: number;
  offset?: number;
}