import React from "react";
import ReactDOM from "react-dom/client";
import moment from "moment";
import "moment/locale/ru";
import "react-big-calendar/lib/css/react-big-calendar.css";

import { App } from "./App";
import "../shared/styles/global.css";
import "../shared/styles/calendar.css";

moment.locale("ru");
moment.updateLocale("ru", { week: { dow: 1 } });

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);