import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/routing": "http://localhost:8000",
      "/feedback": "http://localhost:8000",
      "/agents": "http://localhost:8000"
    }
  }
});


