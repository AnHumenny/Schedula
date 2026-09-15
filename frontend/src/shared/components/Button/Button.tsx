import React from "react";
import styles from "./Button.module.css";

type Variant = "default" | "primary" | "danger" | "ghost";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

export const Button: React.FC<Props> = ({
  variant = "default",
  className = "",
  ...rest
}) => (
  <button
    {...rest}
    className={`${styles.button} ${styles[variant]} ${className}`}
  />
);