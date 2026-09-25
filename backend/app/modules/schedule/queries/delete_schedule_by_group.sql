-- Deprecated: retained for manual testing only.
-- Retained only for manual testing.
-- The working logic has been moved to FastAPI.
-- Parameters and transaction are now handled at the application level.

BEGIN;

WITH settings AS (
    SELECT

        DATE '2026-09-21' AS source_start,
        DATE '2027-03-21' AS source_end,
        12 AS weeks_to_copy,
        1 AS group_id
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
          WHERE sg.schedule_item_id = s.id
            AND sg.group_id = settings.group_id
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


COMMIT;