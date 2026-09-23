BEGIN;        -- TODO: при переносе в FastAPI убрать, транзакцией будет управлять AsyncSession

WITH settings AS (
    SELECT
        -- TODO: при переносе в FastAPI заменить на параметры:
        -- CAST(:source_start AS DATE) AS source_start,
        -- CAST(:source_end AS DATE) AS source_end,
        -- :weeks_to_copy AS weeks_to_copy,
        -- :direction_id AS direction_id,

        DATE '2026-09-14' AS source_start,
        DATE '2026-09-21' AS source_end,
        12 AS weeks_to_copy,
        1 AS direction_id
),

mapping AS (
    SELECT
        s.id AS old_id,
        nextval('public.schedule_items_id_seq') AS new_id,
        week_num
    FROM public.schedule_items AS s
    CROSS JOIN settings
    CROSS JOIN generate_series(
        1,
        settings.weeks_to_copy
    ) AS week_num
    WHERE s.start_datetime >= settings.source_start
      AND s.start_datetime < settings.source_end

      AND EXISTS (
          SELECT 1
          FROM public.schedule_groups AS sg
          JOIN public.groups AS g
              ON g.id = sg.group_id
          WHERE sg.schedule_item_id = s.id
            AND g.direction_id = settings.direction_id
      )
)

SELECT *
INTO TEMP TABLE schedule_item_mapping
FROM mapping;


INSERT INTO public.schedule_items (
    id,
    teacher_id,
    discipline_id,
    room_id,
    start_datetime,
    end_datetime,
    lesson_type,
    status,
    description
)
SELECT
    m.new_id,
    s.teacher_id,
    s.discipline_id,
    s.room_id,
    s.start_datetime + (m.week_num * INTERVAL '7 days'),
    s.end_datetime + (m.week_num * INTERVAL '7 days'),
    s.lesson_type,
    s.status,
    s.description
FROM schedule_item_mapping AS m
JOIN public.schedule_items AS s
    ON s.id = m.old_id;


INSERT INTO public.schedule_groups (
    schedule_item_id,
    group_id
)
SELECT
    m.new_id,
    sg.group_id
FROM schedule_item_mapping AS m
JOIN public.schedule_groups AS sg
    ON sg.schedule_item_id = m.old_id;


INSERT INTO public.schedule_audience (
    schedule_item_id,
    profile_id
)
SELECT
    m.new_id,
    sa.profile_id
FROM schedule_item_mapping AS m
JOIN public.schedule_audience AS sa
    ON sa.schedule_item_id = m.old_id;


COMMIT;       -- TODO: при переносе в FastAPI убрать, транзакцией будет управлять AsyncSession