import React, { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Calendar, momentLocalizer } from "react-big-calendar";
import type { View } from "react-big-calendar";
import moment from "moment";

import { scheduleApi } from "../../shared/api";
import { colorForTeacher } from "../../shared/utils/colors";
import { messages, formats } from "./lib/constants";
import { getCalendarRange } from "./lib/getCalendarRange";
import { useCalendarLookups } from "./hooks/useCalendarLookups";
import {
  useCalendarEvents,
  type CalendarEvent,
} from "./hooks/useCalendarEvents";
import { CustomToolbar } from "./ui/CustomToolbar";
import { CustomDayHeader } from "./ui/CustomDayHeader";
import { EventComponent } from "./ui/EventComponent";
import { EventDetailsModal } from "./ui/EventDetailsModal";
import { CalendarFilters } from "./ui/CalendarFilters";
import { CalendarLegend } from "./ui/CalendarLegend";
import { CalendarStats } from "./ui/CalendarStats";

import styles from "./CalendarView.module.css";

const localizer = momentLocalizer(moment);

type Mode = "admin" | "public";

interface Props {
  mode: Mode;
}

export const CalendarView: React.FC<Props> = ({ mode }) => {
  const navigate = useNavigate();
  const [currentView, setCurrentView] = useState<View>("week");
  const [date, setDate] = useState(new Date());
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [filterGroupId, setFilterGroupId] = useState("");
  const [filterTeacherId, setFilterTeacherId] = useState("");
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(
    null
  );

  const isAdmin = mode === "admin";
  const lookups = useCalendarLookups();

  const range = useMemo(
    () => getCalendarRange(date, currentView),
    [date, currentView]
  );

  const schedule = useQuery({
    queryKey: [
      "schedule",
      "range",
      range.start,
      range.end,
    ],
    queryFn: () =>
      scheduleApi.range({
        start: range.start,
        end: range.end,
      }),
    staleTime: 60_000,
  });

  const rawEvents = useCalendarEvents(schedule.data ?? [], lookups);

  const events = useMemo(() => {
    let result = rawEvents;
    if (filterGroupId) {
      const gid = Number(filterGroupId);
      result = result.filter((e) => e.resource.item.group_ids.includes(gid));
    }
    if (filterTeacherId) {
      const tid = Number(filterTeacherId);
      result = result.filter((e) => e.resource.item.teacher_id === tid);
    }
    return result;
  }, [rawEvents, filterGroupId, filterTeacherId]);

  useEffect(() => {
    const onResize = () => {
      const mobile = window.innerWidth < 768;
      setIsMobile(mobile);
      if (mobile && currentView !== "month") setCurrentView("month");
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, [currentView]);

  const counts = useMemo(() => {
    let planned = 0,
      cancelled = 0,
      rescheduled = 0;
    events.forEach((e) => {
      const s = e.resource.item.status;
      if (s === "PLANNED") planned++;
      else if (s === "CANCELLED") cancelled++;
      else if (s === "RESCHEDULED") rescheduled++;
    });
    return { planned, cancelled, rescheduled };
  }, [events]);

  const teachersInEvents = useMemo(() => {
    const map = new Map<number, string>();
    events.forEach((e) => {
      map.set(e.resource.item.teacher_id, e.resource.teacherName);
    });
    return Array.from(map.entries()).sort((a, b) =>
      a[1].localeCompare(b[1])
    );
  }, [events]);

  const renderEvent = useMemo(
    () =>
      ({ event }: { event: CalendarEvent }) => (
        <EventComponent event={event} isMobile={isMobile} />
      ),
    [isMobile]
  );

  const eventPropGetter = useMemo(
    () => (event: CalendarEvent) => {
      const status = event.resource.item.status;
      return {
        style: {
          backgroundColor: colorForTeacher(event.resource.item.teacher_id),
          border: "none",
          borderRadius: isMobile ? "2px" : "4px",
          padding: isMobile ? "1px 3px" : "2px 6px",
          color: "#1a1d21",
          fontSize: isMobile ? "10px" : "12px",
          cursor: "pointer",
          opacity: status === "CANCELLED" ? 0.5 : 1,
          textDecoration: status === "CANCELLED" ? "line-through" : "none",
          overflow: "hidden",
          width: "100%",
          height: "100%",
        },
      };
    },
    [isMobile]
  );

  const handleDelete = async (item: any) => {
    if (
      !confirm(
        `Удалить занятие «${selectedEvent?.resource.disciplineName}»?`
      )
    )
      return;
    try {
      await scheduleApi.remove(item.id);
      setSelectedEvent(null);
      await schedule.refetch();
    } catch (e) {
      alert((e as Error).message);
    }
  };

  return (
    <div className={styles.container} style={{ padding: isMobile ? 10 : 20 }}>
      <CalendarFilters
        groups={lookups.groups.data ?? []}
        teachers={lookups.teachers.data ?? []}
        filterGroupId={filterGroupId}
        filterTeacherId={filterTeacherId}
        onChangeGroup={setFilterGroupId}
        onChangeTeacher={setFilterTeacherId}
      />

      {schedule.isLoading && (
        <div className={styles.center}>⏳ Загрузка…</div>
      )}

      {schedule.isError && (
        <div className={`${styles.center} ${styles.error}`}>
          ❌ Ошибка: {(schedule.error as Error).message}
        </div>
      )}

      {!schedule.isLoading && !schedule.isError && (
        <>
          {events.length === 0 ? (
            <div className={styles.center}>
              <p style={{ fontSize: 18 }}>📭 Занятий пока нет</p>
              <p style={{ fontSize: 14 }}>
                Выберите другую группу или преподавателя
              </p>
            </div>
          ) : (
            <>
              <div className={styles.calendarWrap}>
                <Calendar
                  localizer={localizer}
                  events={events}
                  startAccessor="start"
                  endAccessor="end"
                  eventPropGetter={eventPropGetter}
                  components={{
                    event: renderEvent,
                    toolbar: CustomToolbar,
                    header: CustomDayHeader,
                  }}
                  formats={formats}
                  style={{ height: "100%" }}
                  date={date}
                  onNavigate={(newDate) => setDate(newDate)}
                  view={currentView}
                  onView={setCurrentView}
                  views={["month", "week", "day", "agenda"]}
                  messages={messages}
                  popup
                  min={new Date(0, 0, 0, 8, 0, 0)}
                  max={new Date(0, 0, 0, 20, 0, 0)}
                  step={5}
                  timeslots={12}
                  selectable={isAdmin}
                  onSelectSlot={
                    isAdmin
                      ? ({ start }) => {
                          const iso = moment(start).format(
                            "YYYY-MM-DDTHH:mm"
                          );
                          navigate(
                            `/schedule/create?start=${encodeURIComponent(
                              iso
                            )}`
                          );
                        }
                      : undefined
                  }
                  onSelectEvent={(event) =>
                    setSelectedEvent(event as CalendarEvent)
                  }
                />
              </div>

              <CalendarLegend
                teachers={teachersInEvents}
                isMobile={isMobile}
              />

              <CalendarStats
                total={events.length}
                planned={counts.planned}
                rescheduled={counts.rescheduled}
                cancelled={counts.cancelled}
                isMobile={isMobile}
                todayLabel={new Date().toLocaleDateString("ru-RU", {
                  day: "2-digit",
                  month: "long",
                  year: "numeric",
                })}
              />
            </>
          )}
        </>
      )}

      {selectedEvent && (
        <EventDetailsModal
          event={selectedEvent}
          onClose={() => setSelectedEvent(null)}
          onEdit={
            isAdmin
              ? (item) => {
                  setSelectedEvent(null);
                  navigate(`/schedule/${item.id}/edit`);
                }
              : undefined
          }
          onDelete={isAdmin ? handleDelete : undefined}
        />
      )}
    </div>
  );
};