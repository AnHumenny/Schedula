BEGIN;        -- TODO: при переносе в FastAPI убрать, транзакцией будет управлять AsyncSession

WITH settings AS (
    SELECT
        -- TODO: при переносе в FastAPI использовать параметры
        -- source_start
        -- source_end
        -- weeks_to_copy
        -- direction_id

        DATE '2026-09-14' AS source_start,
        DATE '2026-09-21' AS source_end,
        12 AS weeks_to_copy,
        1 AS direction_id
),

items_to_delete AS (
    SELECT DISTINCT
        s.id
    FROM public.schedule_items AS s
    CROSS JOIN settings
    WHERE s.start_datetime >= (
        settings.source_start
    )
      AND s.start_datetime < (
        settings.source_end
        + (settings.weeks_to_copy * INTERVAL '7 days')
    )

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
INTO TEMP TABLE schedule_items_to_delete
FROM items_to_delete;


DELETE FROM public.schedule_audience AS sa
WHERE sa.schedule_item_id IN (
    SELECT id
    FROM schedule_items_to_delete
);


DELETE FROM public.schedule_groups AS sg
WHERE sg.schedule_item_id IN (
    SELECT id
    FROM schedule_items_to_delete
);


DELETE FROM public.schedule_items AS s
WHERE s.id IN (
    SELECT id
    FROM schedule_items_to_delete
);


COMMIT;       -- TODO: при переносе в FastAPI убрать, транзакцией будет управлять AsyncSession