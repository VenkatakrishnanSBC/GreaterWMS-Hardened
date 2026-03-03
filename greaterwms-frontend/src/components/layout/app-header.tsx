"use client";

import { useAuthStore } from "@/stores/auth-store";
import { Bolt, Languages } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";

const languages = [
    { code: "en-US", label: "English" },
    { code: "zh-hans", label: "中文简体" },
    { code: "zh-hant", label: "中文繁體" },
    { code: "fr", label: "Français" },
    { code: "pt", label: "Português" },
    { code: "sp", label: "Español" },
    { code: "de", label: "Deutsch" },
    { code: "ru", label: "Русский" },
    { code: "ar", label: "العربية" },
    { code: "it", label: "Italiano" },
    { code: "ja", label: "日本語" },
];

export function AppHeader() {
    const { warehouseName } = useAuthStore();

    return (
        <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 px-6">
            <div className="flex-1">
                <h1 className="text-lg font-semibold">
                    {warehouseName || "GreaterWMS"}
                </h1>
            </div>

            <div className="flex items-center gap-2">
                {/* Language Selector */}
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon">
                            <Languages className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-40">
                        {languages.map((lang) => (
                            <DropdownMenuItem key={lang.code}>
                                {lang.label}
                            </DropdownMenuItem>
                        ))}
                    </DropdownMenuContent>
                </DropdownMenu>

                {/* API Docs Link */}
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => window.open("/api/docs/", "_blank")}
                >
                    <Bolt className="h-4 w-4" />
                </Button>

                {/* Version Badge */}
                <Badge variant="outline" className="text-xs font-normal">
                    v3.0
                </Badge>
            </div>
        </header>
    );
}
