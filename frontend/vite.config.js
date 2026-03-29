// import { defineConfig } from 'vite'
// import { svelte } from '@sveltejs/vite-plugin-svelte'
//
// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [svelte()],
// })

import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { resolve } from 'path'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  base: '/static/svelte/assets/',
  plugins: [tailwindcss(), svelte()],
  resolve: {
    alias: {
      fonts: resolve('../static/svelte/fonts'),
      svg: resolve('../static/svelte/svg'),
    },
  },
  build: {
    outDir: resolve('../main/static/svelte/assets'),
    assetsDir: '',
    chunkSizeWarningLimit: 1000,
    manifest: true,
    emptyOutDir: true,
    watch: {},
  },
  server: {
    watch: {
      usePolling: true,
      interval: 100,
    },
    port: 8000,
    hot: true,
  },
});

