import React from "react";
import { Modal } from "../Modal/Modal";
import { Button } from "../Button/Button";
import styles from "./FormModal.module.css";

interface Props {
  open: boolean;
  title: string;
  onClose: () => void;
  onSubmit: () => void;
  saving?: boolean;
  error?: Error | null;
  submitLabel?: string;
  children: React.ReactNode;
}

export const FormModal: React.FC<Props> = ({
  open,
  title,
  onClose,
  onSubmit,
  saving,
  error,
  submitLabel = "Сохранить",
  children,
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <Modal open={open} title={title} onClose={onClose}>
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.fields}>{children}</div>

        <div className={styles.actions}>
          <Button type="button" onClick={onClose}>
            Отмена
          </Button>
          <Button type="submit" variant="primary" disabled={saving}>
            {saving ? "Сохранение…" : submitLabel}
          </Button>
        </div>

        {error && <p className="error">{error.message}</p>}
      </form>
    </Modal>
  );
};