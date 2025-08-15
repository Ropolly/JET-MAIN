import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import postcssPresetMantine from 'postcss-preset-mantine'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: {
      plugins: [
        postcssPresetMantine(),
      ],
    },
  },
})
