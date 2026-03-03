"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    BarChart3,
    PackageCheck,
    Send,
    Archive,
    ScanBarcode,
    Landmark,
    Banknote,
    UsersRound,
    CarFront,
    ArrowUpFromLine,
    ArrowDownToLine,
    Moon,
    Sun,
    LogOut,
    ChevronLeft,
    Boxes,
    Warehouse,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { useAuthStore } from "@/stores/auth-store";
import { useState } from "react";

const navItems = [
    { name: "Dashboard", href: "/dashboard", icon: BarChart3 },
    { type: "separator" as const },
    { name: "Inbound", href: "/inbound/asn", icon: PackageCheck },
    { name: "Outbound", href: "/outbound/dn", icon: Send },
    { name: "Stock", href: "/stock/list", icon: Archive },
    { type: "separator" as const },
    { name: "Finance", href: "/finance/capital", icon: Banknote },
    { name: "Goods", href: "/goods/list", icon: ScanBarcode },
    { name: "Base Info", href: "/baseinfo/company", icon: Landmark },
    { name: "Warehouse", href: "/warehouse/settings", icon: Warehouse },
    { type: "separator" as const },
    { name: "Staff", href: "/staff/list", icon: UsersRound },
    { name: "Drivers", href: "/driver/list", icon: CarFront },
    { type: "separator" as const },
    { name: "Upload", href: "/upload", icon: ArrowUpFromLine },
    { name: "Download", href: "/download", icon: ArrowDownToLine },
];

export function AppSidebar() {
    const pathname = usePathname();
    const { theme, setTheme } = useTheme();
    const { loginName, logout } = useAuthStore();
    const [collapsed, setCollapsed] = useState(false);

    return (
        <aside
            className={cn(
                "flex h-screen flex-col border-r bg-sidebar text-sidebar-foreground transition-all duration-300",
                collapsed ? "w-16" : "w-60"
            )}
        >
            {/* Logo */}
            <div className="flex h-14 items-center border-b px-4">
                {!collapsed && (
                    <Link href="/dashboard" className="flex items-center gap-2">
                        <Boxes className="h-6 w-6 text-primary" />
                        <span className="text-lg font-bold bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">
                            GreaterWMS
                        </span>
                    </Link>
                )}
                <Button
                    variant="ghost"
                    size="icon"
                    className={cn("ml-auto h-8 w-8", collapsed && "mx-auto")}
                    onClick={() => setCollapsed(!collapsed)}
                >
                    <ChevronLeft
                        className={cn(
                            "h-4 w-4 transition-transform",
                            collapsed && "rotate-180"
                        )}
                    />
                </Button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 overflow-y-auto p-2">
                <ul className="space-y-1">
                    {navItems.map((item, i) => {
                        if ("type" in item && item.type === "separator") {
                            return <li key={i} className="my-2 border-t border-border/50" />;
                        }
                        const navItem = item as {
                            name: string;
                            href: string;
                            icon: React.ComponentType<{ className?: string }>;
                        };
                        const Icon = navItem.icon;
                        const isActive =
                            pathname === navItem.href ||
                            pathname.startsWith(navItem.href.split("/").slice(0, 2).join("/") + "/");

                        return (
                            <li key={navItem.href}>
                                <Link
                                    href={navItem.href}
                                    className={cn(
                                        "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                                        isActive
                                            ? "bg-primary/10 text-primary"
                                            : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                                    )}
                                    title={navItem.name}
                                >
                                    <Icon className="h-4 w-4 shrink-0" />
                                    {!collapsed && <span>{navItem.name}</span>}
                                </Link>
                            </li>
                        );
                    })}
                </ul>
            </nav>

            {/* Footer */}
            <div className="border-t p-2 space-y-1">
                <Button
                    variant="ghost"
                    size={collapsed ? "icon" : "default"}
                    className={cn("w-full", !collapsed && "justify-start gap-2")}
                    onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                >
                    {theme === "dark" ? (
                        <Sun className="h-4 w-4" />
                    ) : (
                        <Moon className="h-4 w-4" />
                    )}
                    {!collapsed && (
                        <span>{theme === "dark" ? "Light Mode" : "Dark Mode"}</span>
                    )}
                </Button>
                {!collapsed && loginName && (
                    <div className="flex items-center gap-2 px-3 py-2 text-xs text-muted-foreground">
                        <div className="h-6 w-6 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-xs">
                            {loginName.charAt(0).toUpperCase()}
                        </div>
                        <span className="truncate">{loginName}</span>
                    </div>
                )}
                <Button
                    variant="ghost"
                    size={collapsed ? "icon" : "default"}
                    className={cn(
                        "w-full text-destructive hover:text-destructive",
                        !collapsed && "justify-start gap-2"
                    )}
                    onClick={logout}
                >
                    <LogOut className="h-4 w-4" />
                    {!collapsed && <span>Logout</span>}
                </Button>
            </div>
        </aside>
    );
}
