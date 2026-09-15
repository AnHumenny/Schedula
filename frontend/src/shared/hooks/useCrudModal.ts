import { useCallback, useState } from "react";

export function useCrudModal<T extends Record<string, any>>(initial: T) {
  const [open, setOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [values, setValues] = useState<T>(initial);

  const reset = useCallback(() => {
    setEditingId(null);
    setValues(initial);
  }, [initial]);

  const openCreate = useCallback(() => {
    reset();
    setOpen(true);
  }, [reset]);

  const openEdit = useCallback(
    (id: number, item: Partial<T>) => {
      setEditingId(id);
      setValues({ ...initial, ...item });
      setOpen(true);
    },
    [initial]
  );

  const close = useCallback(() => {
    setOpen(false);
    reset();
  }, [reset]);

  const setField = useCallback(
    <K extends keyof T>(key: K, value: T[K]) => {
      setValues((prev) => ({ ...prev, [key]: value }));
    },
    []
  );

  return {
    open,
    editingId,
    values,
    setField,
    setValues,
    openCreate,
    openEdit,
    close,
  };
}