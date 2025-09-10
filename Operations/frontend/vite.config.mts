import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
// import basicSsl from "@vitejs/plugin-basic-ssl"; // Disabled for HTTP mode

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // Uncomment below to enable HTTPS with SSL certificates
    // basicSsl({
    //   name: "localhost",
    //   domains: ["localhost", "127.0.0.1", "::1"],
    //   certDir: "./certs"
    // })
  ],
  resolve: {
    alias: {
      "vue-i18n": "vue-i18n/dist/vue-i18n.cjs.js",
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  base: "/",
  build: {
    chunkSizeWarningLimit: 3000,
  },
  server: {
    host: "localhost",
    port: 5173,
  },
});
