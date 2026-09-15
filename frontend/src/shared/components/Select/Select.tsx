import React from "react";
import styles from "./Select.module.css";

export interface SelectOption {
  value: string | number;
  label: string;
}

interface Props {
  label?: string;
  value: string | number;
  onChange: (value: string) => void;
  options: SelectOption[];
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
}

export const Select: React.FC<Props> = ({
  label,
  value,
  onChange,
  options,
  placeholder,
  required,
  disabled,
  className,
}) => (
  <label className={`${styles.field} ${className ?? ""}`}>
    {label && <span className={styles.label}>{label}</span>}
    <select
      className={styles.select}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      required={required}
      disabled={disabled}
    >
      {placeholder && <option value="">{placeholder}</option>}
      {options.map((o) => (
        <option key={o.value} value={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  </label>
);