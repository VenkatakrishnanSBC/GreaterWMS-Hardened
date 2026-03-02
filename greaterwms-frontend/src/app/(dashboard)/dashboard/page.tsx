"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
    PackagePlus,
    Truck,
    Layers,
    AlertTriangle,
    TrendingUp,
    TrendingDown,
    ArrowUpRight,
    ArrowDownRight,
} from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api-client";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area,
} from "recharts";

interface StatsCardProps {
    title: string;
    value: string | number;
    change?: string;
    trend?: "up" | "down";
    icon: React.ComponentType<{ className?: string }>;
}

function StatsCard({ title, value, change, trend, icon: Icon }: StatsCardProps) {
    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                    {title}
                </CardTitle>
                <div className="rounded-md bg-primary/10 p-2">
                    <Icon className="h-4 w-4 text-primary" />
                </div>
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{value}</div>
                {change && (
                    <p className="text-xs text-muted-foreground flex items-center gap-1 mt-1">
                        {trend === "up" ? (
                            <ArrowUpRight className="h-3 w-3 text-emerald-500" />
                        ) : (
                            <ArrowDownRight className="h-3 w-3 text-red-500" />
                        )}
                        <span className={trend === "up" ? "text-emerald-500" : "text-red-500"}>
                            {change}
                        </span>{" "}
                        from last month
                    </p>
                )}
            </CardContent>
        </Card>
    );
}

// Demo chart data
const chartData = [
    { name: "Mon", inbound: 40, outbound: 24 },
    { name: "Tue", inbound: 30, outbound: 13 },
    { name: "Wed", inbound: 20, outbound: 38 },
    { name: "Thu", inbound: 27, outbound: 39 },
    { name: "Fri", inbound: 18, outbound: 48 },
    { name: "Sat", inbound: 23, outbound: 38 },
    { name: "Sun", inbound: 34, outbound: 43 },
];

const areaData = [
    { name: "Jan", value: 400 },
    { name: "Feb", value: 300 },
    { name: "Mar", value: 500 },
    { name: "Apr", value: 280 },
    { name: "May", value: 590 },
    { name: "Jun", value: 430 },
    { name: "Jul", value: 640 },
];

export default function DashboardPage() {
    const { data: stats, isLoading } = useQuery({
        queryKey: ["dashboard-stats"],
        queryFn: async () => {
            try {
                const res = await api.get<{ total_inbound: number; total_outbound: number }>(
                    "dashboard/stats/"
                );
                return res;
            } catch {
                return { total_inbound: 0, total_outbound: 0 };
            }
        },
    });

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
                <p className="text-muted-foreground">
                    Warehouse performance overview and analytics
                </p>
            </div>

            {/* Stats Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {isLoading ? (
                    Array.from({ length: 4 }).map((_, i) => (
                        <Card key={i}>
                            <CardContent className="p-6">
                                <Skeleton className="h-4 w-24 mb-3" />
                                <Skeleton className="h-8 w-16" />
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <>
                        <StatsCard
                            title="Total Inbound"
                            value={stats?.total_inbound || 0}
                            change="+12%"
                            trend="up"
                            icon={PackagePlus}
                        />
                        <StatsCard
                            title="Total Outbound"
                            value={stats?.total_outbound || 0}
                            change="+8%"
                            trend="up"
                            icon={Truck}
                        />
                        <StatsCard
                            title="Stock Items"
                            value="2,847"
                            change="-3%"
                            trend="down"
                            icon={Layers}
                        />
                        <StatsCard
                            title="Alerts"
                            value="12"
                            change="+2"
                            trend="up"
                            icon={AlertTriangle}
                        />
                    </>
                )}
            </div>

            {/* Charts */}
            <div className="grid gap-4 lg:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <TrendingUp className="h-5 w-5 text-primary" />
                            Inbound vs Outbound
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Tabs defaultValue="bar">
                            <TabsList>
                                <TabsTrigger value="bar">Bar</TabsTrigger>
                                <TabsTrigger value="area">Area</TabsTrigger>
                            </TabsList>
                            <TabsContent value="bar" className="mt-4">
                                <ResponsiveContainer width="100%" height={300}>
                                    <BarChart data={chartData}>
                                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                                        <XAxis dataKey="name" className="text-xs" />
                                        <YAxis className="text-xs" />
                                        <Tooltip
                                            contentStyle={{
                                                backgroundColor: "hsl(var(--card))",
                                                border: "1px solid hsl(var(--border))",
                                                borderRadius: "8px",
                                            }}
                                        />
                                        <Bar dataKey="inbound" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
                                        <Bar dataKey="outbound" fill="hsl(var(--primary) / 0.5)" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </TabsContent>
                            <TabsContent value="area" className="mt-4">
                                <ResponsiveContainer width="100%" height={300}>
                                    <AreaChart data={chartData}>
                                        <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                                        <XAxis dataKey="name" />
                                        <YAxis />
                                        <Tooltip />
                                        <Area type="monotone" dataKey="inbound" stroke="hsl(var(--primary))" fill="hsl(var(--primary) / 0.2)" />
                                        <Area type="monotone" dataKey="outbound" stroke="hsl(var(--destructive))" fill="hsl(var(--destructive) / 0.2)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </TabsContent>
                        </Tabs>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <TrendingDown className="h-5 w-5 text-primary" />
                            Stock Trend
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <ResponsiveContainer width="100%" height={350}>
                            <AreaChart data={areaData}>
                                <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
                                <XAxis dataKey="name" className="text-xs" />
                                <YAxis className="text-xs" />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: "hsl(var(--card))",
                                        border: "1px solid hsl(var(--border))",
                                        borderRadius: "8px",
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="value"
                                    stroke="hsl(var(--primary))"
                                    fill="hsl(var(--primary) / 0.15)"
                                    strokeWidth={2}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
