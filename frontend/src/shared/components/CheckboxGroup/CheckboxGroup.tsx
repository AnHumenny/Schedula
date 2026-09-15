import React from "react";
import styles from "./CheckboxGroup.module.css";

export interface CheckboxOption {
  value: number;
  label: string;
}

interface Props {
  label?: string;
  values: number[];
  onChange: (values: number[]) => void;
  options: CheckboxOption[];
  emptyText?: string;
  disabled?: boolean;
}

export const CheckboxGroup: React.FC<Props> = ({
  label,
  values,
  onChange,
  options,
  emptyText = "Нет вариантов",
  disabled,
}) => {
  const toggle = (id: number) => {
    if (disabled) return;
    onChange(
      values.includes(id) ? values.filter((x) => x !== id) : [...values, id]
    );
  };

  return (
    <div className={styles.field}>
      {label && (
        <span className={styles.label}>
          {label} — выбрано: {values.length}
        </span>
      )}
      <div className={styles.list}>
        {options.map((o) => (
          <label key={o.value} className={styles.item}>
            <input
              type="checkbox"
              checked={values.includes(o.value)}
              onChange={() => toggle(o.value)}
              disabled={disabled}
            />
            <span>{o.label}</span>
          </label>
        ))}
        {options.length === 0 && (
          <span className="muted">{emptyText}</span>
        )}
      </div>
    </div>
  );
};