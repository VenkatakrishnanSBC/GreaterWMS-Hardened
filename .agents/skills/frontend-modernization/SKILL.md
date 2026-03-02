---
name: frontend-modernization
description: Vue 3/Quasar v2 migration, frontend testing, Axios interceptors, build optimization
---

# Frontend Modernization Skill

Use this skill when implementing TODO items FRONT-001 through FRONT-004 or UPGRADE-002, or fixing issues ISS-016, ISS-018.

## 1. Quasar v1 → v2 Migration Path

```
Phase 1: Prepare (non-breaking)
├── Audit all components for Vue 2 deprecated APIs
├── Replace .sync modifiers with v-model
├── Replace $listeners with v-bind="$attrs"
└── Update event handling to v3 patterns

Phase 2: Framework upgrade
├── Update package.json: quasar@2.x, @quasar/app-vite
├── Migrate from Webpack to Vite (Quasar v2 default)
├── Update boot files and plugins
└── Migrate store from Vuex to Pinia

Phase 3: Component migration
├── Update Quasar component APIs (breaking changes)
├── Migrate vue-i18n from v8 to v9
├── Migrate vue-echarts to v6 (Vue 3 compatible)
└── Test all pages and flows
```

## 2. Frontend Test Setup

```json
// package.json additions
{
  "devDependencies": {
    "@vue/test-utils": "^2.0.0",
    "vitest": "^1.0.0",
    "@testing-library/vue": "^8.0.0"
  },
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

## 3. Axios Interceptors

```javascript
// src/boot/axios.js
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.API_URL || 'http://localhost:8008',
  timeout: 30000,
})

// Request interceptor — inject auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('openid')
  if (token) {
    config.headers['Token'] = token
  }
  config.headers['Language'] = localStorage.getItem('language') || 'en'
  return config
})

// Response interceptor — handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('openid')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

## 4. Cache-Busting Fix

```javascript
// quasar.config.js
module.exports = {
  build: {
    // Add content hash to filenames for cache busting
    extendWebpack(cfg) {
      cfg.output.filename = 'js/[name].[contenthash:8].js'
      cfg.output.chunkFilename = 'js/[name].[contenthash:8].js'
    }
  }
}
```

## 5. ESLint Update

```json
{
  "devDependencies": {
    "eslint": "^8.0.0",
    "eslint-plugin-vue": "^9.0.0",
    "@vue/eslint-config-standard": "^8.0.0"
  }
}
```

## Verification
```bash
# Build succeeds:
cd templates && npm run build

# Tests pass:
npm test

# Lint passes:
npm run lint

# No console errors in browser
```
