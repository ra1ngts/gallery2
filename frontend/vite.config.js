import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ command }) => {
  return {
    base: '/static/svelte/assets/',
    plugins: [tailwindcss(), svelte()],
    resolve: {
      alias: {
        fonts: resolve('./public/fonts'), 
        svg: resolve('../static/svelte/svg'),
      },
    },
    build: {
      outDir: resolve('../main/static/svelte/assets'),
      assetsDir: '',
      chunkSizeWarningLimit: 1000,
      manifest: true,
      emptyOutDir: true,
      watch: command === 'serve' ? {} : null,
    },
    server: {
      watch: {
        usePolling: true,
        interval: 100,
      },
      port: 8000,
      hot: true,
    },
  };
});
