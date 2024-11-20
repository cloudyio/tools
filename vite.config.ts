import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    build: {
        sourcemap: process.env.NODE_ENV === 'development'
    },
    server: {
        fs: {
            strict: false // This can help with some path resolution issues
        },
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        }
    }
});
