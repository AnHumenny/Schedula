import React from "react";
import { RouterProvider } from "react-router-dom";
import { QueryProvider } from "./providers/QueryProvider";
import { router } from "./router";

export const App: React.FC = () => (
  <QueryProvider>
    <RouterProvider router={router} />
  </QueryProvider>
);