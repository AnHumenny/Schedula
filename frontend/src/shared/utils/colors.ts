import { TEACHER_COLORS } from "../constants/calendar";

export const colorForTeacher = (teacherId: number): string =>
  TEACHER_COLORS[teacherId % TEACHER_COLORS.length];