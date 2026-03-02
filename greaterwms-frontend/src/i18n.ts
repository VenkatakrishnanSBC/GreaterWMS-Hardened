"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import enMessages from "@/messages/en.json";

export const locales = [
    { code: "en", label: "English" },
    { code: "zh-hans", label: "中文简体" },
    { code: "zh-hant", label: "中文繁體" },
    { code: "fr", label: "Français" },
    { code: "de", label: "Deutsch" },
    { code: "pt", label: "Português" },
    { code: "sp", label: "Español" },
    { code: "ru", label: "Русский" },
    { code: "ar", label: "العربية" },
    { code: "it", label: "Italiano" },
    { code: "ja", label: "日本語" },
] as const;

export type Locale = (typeof locales)[number]["code"];

type Messages = typeof enMessages;

interface I18nState {
    locale: Locale;
    messages: Messages;
    setLocale: (locale: Locale) => void;
}

// Helper to get nested value from dot-separated key
function getNestedValue(obj: Record<string, unknown>, key: string): string {
    const parts = key.split(".");
    let current: unknown = obj;
    for (const part of parts) {
        if (current && typeof current === "object" && part in current) {
            current = (current as Record<string, unknown>)[part];
        } else {
            return key; // fallback to key
        }
    }
    return typeof current === "string" ? current : key;
}

export const useI18nStore = create<I18nState>()(
    persist(
        (set) => ({
            locale: "en",
            messages: enMessages,
            setLocale: async (locale: Locale) => {
                try {
                    const msgs = await import(`@/messages/${locale}.json`);
                    set({ locale, messages: msgs.default });
                } catch {
                    // Fallback to English if translation file doesn't exist
                    set({ locale, messages: enMessages });
                }
            },
        }),
        { name: "gwms-locale", partialize: (state) => ({ locale: state.locale }) }
    )
);

export function useTranslation() {
    const { messages } = useI18nStore();
    const t = (key: string) => getNestedValue(messages as unknown as Record<string, unknown>, key);
    return { t };
}
