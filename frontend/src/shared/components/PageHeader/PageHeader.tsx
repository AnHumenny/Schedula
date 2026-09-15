import React from "react";
import styles from "./PageHeader.module.css";

interface Props {
  title: string;
  children?: React.ReactNode;
}

export const PageHeader: React.FC<Props> = ({ title, children }) => (
  <div className={styles.header}>
    <h1 className={styles.title}>{title}</h1>
    {children && <div className={styles.actions}>{children}</div>}
  </div>
);