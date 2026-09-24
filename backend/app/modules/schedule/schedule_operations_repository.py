from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class ScheduleOperationsRepository:
    """Repository for managing schedule item data persistence."""

    def __init__(self, session: AsyncSession):
        """Initialize the schedule repository."""
        self.session = session

    async def copy_by_group(
        self,
        source_start: date,
        source_end: date,
        weeks_to_copy: int,
        group_id: int,
    ) -> None:
        """Copies the group’s classes for weeks_to_copy weeks ahead.

        Takes the classes of group group_id from the period (source_start, source_end)
        and creates copies of them with a shift of x..weeks_to_copy weeks.
        The transaction is in the calling code.
        """

        params = {
            "source_start": source_start,
            "source_end": source_end,
            "weeks_to_copy": weeks_to_copy,
            "group_id": group_id,
        }

        await self.session.execute(
            text("""
                CREATE TEMP TABLE schedule_item_mapping ON COMMIT DROP AS
                WITH settings AS (
                    SELECT
                        CAST(:source_start  AS date) AS source_start,
                        CAST(:source_end    AS date) AS source_end,
                        CAST(:weeks_to_copy AS int)  AS weeks_to_copy,
                        CAST(:group_id      AS int)  AS group_id
                )
                SELECT
                    s.id AS old_id,
                    nextval('public.schedule_items_id_seq') AS new_id,
                    week_num,
                    settings.group_id
                FROM public.schedule_items AS s
                CROSS JOIN settings
                CROSS JOIN generate_series(1, settings.weeks_to_copy) AS week_num
                WHERE s.start_datetime >= settings.source_start
                  AND s.start_datetime <  settings.source_end
                  AND EXISTS (
                      SELECT 1
                      FROM public.schedule_groups AS sg
                      WHERE sg.schedule_item_id = s.id
                        AND sg.group_id = settings.group_id
                  );
            """),
            params,
        )

        await self.session.execute(text("""
            INSERT INTO public.schedule_items (
                id, teacher_id, discipline_id, room_id,
                start_datetime, end_datetime,
                lesson_type, status, description
            )
            SELECT
                m.new_id,
                s.teacher_id,
                s.discipline_id,
                s.room_id,
                s.start_datetime + (m.week_num * INTERVAL '7 days'),
                s.end_datetime   + (m.week_num * INTERVAL '7 days'),
                s.lesson_type,
                s.status,
                s.description
            FROM schedule_item_mapping AS m
            JOIN public.schedule_items AS s ON s.id = m.old_id;
        """))

        await self.session.execute(text("""
            INSERT INTO public.schedule_groups (schedule_item_id, group_id)
            SELECT m.new_id, m.group_id
            FROM schedule_item_mapping AS m;
        """))

        await self.session.execute(text("""
            INSERT INTO public.schedule_audience (schedule_item_id, profile_id)
            SELECT m.new_id, sa.profile_id
            FROM schedule_item_mapping AS m
            JOIN public.schedule_audience AS sa
                ON sa.schedule_item_id = m.old_id;
        """))



    async def copy_by_direction(
            self,
            source_start: date,
            source_end: date,
            weeks_to_copy: int,
            direction_id: int,
    ) -> None:
        """Copies the classes of all groups of the direction direction_id

        from the period (source_start, source_end) to weeks_to_copy weeks ahead.
        The commit is on the calling code.
        """

        params = {
            "source_start": source_start,
            "source_end": source_end,
            "weeks_to_copy": weeks_to_copy,
            "direction_id": direction_id,
        }

        await self.session.execute(
            text("""
                CREATE TEMP TABLE schedule_item_mapping ON COMMIT DROP AS
                WITH settings AS (
                    SELECT
                        CAST(:source_start  AS date) AS source_start,
                        CAST(:source_end    AS date) AS source_end,
                        CAST(:weeks_to_copy AS int)  AS weeks_to_copy,
                        CAST(:direction_id  AS int)  AS direction_id
                )
                SELECT
                    s.id AS old_id,
                    nextval('public.schedule_items_id_seq') AS new_id,
                    week_num
                FROM public.schedule_items AS s
                CROSS JOIN settings
                CROSS JOIN generate_series(1, settings.weeks_to_copy) AS week_num
                WHERE s.start_datetime >= settings.source_start
                  AND s.start_datetime <  settings.source_end
                  AND EXISTS (
                      SELECT 1
                      FROM public.schedule_groups AS sg
                      JOIN public.groups AS g
                          ON g.id = sg.group_id
                      WHERE sg.schedule_item_id = s.id
                        AND g.direction_id = settings.direction_id
                  );
            """),
            params,
        )

        await self.session.execute(text("""
            INSERT INTO public.schedule_items (
                id, teacher_id, discipline_id, room_id,
                start_datetime, end_datetime,
                lesson_type, status, description
            )
            SELECT
                m.new_id,
                s.teacher_id,
                s.discipline_id,
                s.room_id,
                s.start_datetime + (m.week_num * INTERVAL '7 days'),
                s.end_datetime   + (m.week_num * INTERVAL '7 days'),
                s.lesson_type,
                s.status,
                s.description
            FROM schedule_item_mapping AS m
            JOIN public.schedule_items AS s ON s.id = m.old_id;
        """))

        await self.session.execute(text("""
            INSERT INTO public.schedule_groups (schedule_item_id, group_id)
            SELECT
                m.new_id,
                sg.group_id
            FROM schedule_item_mapping AS m
            JOIN public.schedule_groups AS sg
                ON sg.schedule_item_id = m.old_id;
        """))

        await self.session.execute(text("""
            INSERT INTO public.schedule_audience (schedule_item_id, profile_id)
            SELECT
                m.new_id,
                sa.profile_id
            FROM schedule_item_mapping AS m
            JOIN public.schedule_audience AS sa
                ON sa.schedule_item_id = m.old_id;
        """))
