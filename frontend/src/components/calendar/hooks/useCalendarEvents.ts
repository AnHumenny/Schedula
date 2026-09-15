import { useMemo } from "react";
import type { ScheduleItem } from "../../../shared/types";
import {
  LESSON_TYPE_LABELS,
  LESSON_STATUS_LABELS,
} from "../../../shared/constants";
import type { useCalendarLookups } from "./useCalendarLookups";

export interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  allDay: boolean;
  resource: {
    item: ScheduleItem;
    disciplineName: string;
    teacherName: string;
    roomLabel: string;
    groupNames: string;
    lessonTypeLabel: string;
    statusLabel: string;
  };
}

export function useCalendarEvents(
  items: ScheduleItem[],
  lookups: ReturnType<typeof useCalendarLookups>
): CalendarEvent[] {
  const { disciplineById, teacherById, groupById, roomLabel } = lookups;

  return useMemo(() => {
    return items.map((item) => ({
      id: String(item.id),
      title:
        (disciplineById.get(item.discipline_id) ??
          `Дисциплина #${item.discipline_id}`) +
        (item.description ? ` · ${item.description}` : ""),
      start: new Date(item.start_datetime),
      end: new Date(item.end_datetime),
      allDay: false,
      resource: {
        item,
        disciplineName:
          disciplineById.get(item.discipline_id) ??
          `#${item.discipline_id}`,
        teacherName:
          teacherById.get(item.teacher_id) ?? `#${item.teacher_id}`,
        roomLabel: roomLabel(item.room_id),
        groupNames:
          item.group_ids
            .map((id) => groupById.get(id) ?? `#${id}`)
            .join(", ") || "—",
        lessonTypeLabel:
          LESSON_TYPE_LABELS[item.lesson_type] ?? item.lesson_type,
        statusLabel: LESSON_STATUS_LABELS[item.status] ?? item.status,
      },
    }));
  }, [items, disciplineById, teacherById, groupById, roomLabel]);
}