"""
UPGRADE-001/002/003: Django 5.x, Vue 3, and Bomiot compatibility preparation.

This module documents the changes needed for major framework upgrades
and provides compatibility shims for gradual migration.
"""

# ============================================================
# UPGRADE-001: Django 4.1 → Django 5.x Compatibility Notes
# ============================================================
#
# Breaking changes to address before upgrading:
#
# 1. DEFAULT_AUTO_FIELD (already set to BigAutoField ✅)
# 2. CSRF_TRUSTED_ORIGINS must include scheme (already done ✅)
# 3. django.utils.timezone.utc → datetime.timezone.utc
# 4. url() → path()/re_path() (already using path() ✅)
# 5. NullBooleanField → BooleanField(null=True) (not used ✅)
# 6. STATICFILES_STORAGE → STORAGES dict (Django 5.1+)
#
# New Django 5.x features to leverage:
# - Field groups in forms
# - Simplified templates for form rendering
# - Database-computed default values
# - Generated model fields
# - Facet filters in admin
#

DJANGO5_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ============================================================
# UPGRADE-002: Vue 2 → Vue 3 + Quasar v2 Migration Notes
# ============================================================
#
# Key migration steps:
#
# 1. Replace `new Vue()` with `createApp()`
# 2. Update Vuex 3 → Pinia (or Vuex 4)
# 3. Update Vue Router 3 → Vue Router 4
# 4. Replace `Vue.prototype.$axios` with `app.config.globalProperties`
# 5. Update event bus (Bus.$emit) → mitt or provide/inject
# 6. Update Quasar v1 → v2:
#    - Import changes (useQuasar composable)
#    - Component API changes
#    - Boot files update
# 7. Update vue-i18n v8 → v9 (Composition API)
# 8. Replace Options API components with Composition API (optional)
#
# Suggested migration order:
# Phase 1: Update build tools (Vite replaces Webpack)
# Phase 2: Migrate router + state management
# Phase 3: Migrate components (one at a time)
# Phase 4: Migrate boot files
# Phase 5: Full testing pass
#

# ============================================================
# UPGRADE-003: Bomiot Framework Preparation
# ============================================================
#
# Bomiot is the v3.0 reconstruction of GreaterWMS.
# Key architectural changes:
#
# 1. Event-driven architecture
# 2. Plugin system for modular features
# 3. Real-time WebSocket updates
# 4. GraphQL API alongside REST
# 5. Micro-frontend architecture
# 6. Kubernetes-native deployment
#
# Preparation steps:
# 1. Document all current API endpoints
# 2. Create API compatibility layer
# 3. Design event schemas
# 4. Plan data migration scripts
#

# Compatibility helpers for gradual migration

def get_storages_config(use_whitenoise: bool = True) -> dict:
    """
    Get Django 5.x STORAGES config (replaces STATICFILES_STORAGE).

    Use this when upgrading to Django 5.1+:
        STORAGES = get_storages_config()
    """
    config = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
    if use_whitenoise:
        config["staticfiles"] = {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        }
    else:
        config["staticfiles"] = {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        }
    return config
