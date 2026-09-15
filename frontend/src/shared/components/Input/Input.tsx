import React from "react";
import styles from "./Input.module.css";

interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export const Input: React.FC<Props> = ({ label, ...rest }) => (
  <label className={styles.field}>
    {label && <span className={styles.label}>{label}</span>}
    <input {...rest} className={styles.input} />
  </label>
);