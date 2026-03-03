"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Boxes } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useAuthStore } from "@/stores/auth-store";
import { api } from "@/lib/api-client";
import { toast } from "sonner";

export default function LoginPage() {
    const router = useRouter();
    const { login } = useAuthStore();
    const [isLoading, setIsLoading] = useState(false);

    // Admin login
    const [adminName, setAdminName] = useState("");
    const [adminPassword, setAdminPassword] = useState("");

    // User login
    const [staffName, setStaffName] = useState("");
    const [checkCode, setCheckCode] = useState("");

    const handleAdminLogin = async () => {
        setIsLoading(true);
        try {
            const res = await api.post<{ detail: string; openid?: string; token?: string }>(
                "login/",
                { name: adminName, password: adminPassword }
            );
            login({ openid: res.openid || "", loginName: adminName, loginId: 0, staffType: "Admin" });
            router.push("/dashboard");
        } catch (err: unknown) {
            const error = err as { detail?: string };
            toast.error(error.detail || "Login failed");
        } finally {
            setIsLoading(false);
        }
    };

    const handleUserLogin = async () => {
        setIsLoading(true);
        try {
            const res = await api.post<{ detail: string; openid?: string }>(
                "login/",
                { name: staffName, check_code: Number(checkCode) }
            );
            login({ openid: res.openid || "", loginName: staffName, loginId: 0 });
            router.push("/dashboard");
        } catch (err: unknown) {
            const error = err as { detail?: string };
            toast.error(error.detail || "Login failed");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
            <div className="w-full max-w-md space-y-6">
                {/* Logo */}
                <div className="text-center space-y-2">
                    <div className="inline-flex items-center justify-center rounded-xl bg-primary/10 p-3">
                        <Boxes className="h-8 w-8 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">
                        GreaterWMS
                    </h1>
                    <p className="text-sm text-muted-foreground">
                        Warehouse Management System
                    </p>
                </div>

                {/* Login Card */}
                <Card className="border-border/50 shadow-2xl">
                    <Tabs defaultValue="admin">
                        <CardHeader className="pb-3">
                            <TabsList className="grid w-full grid-cols-2">
                                <TabsTrigger value="admin">Admin Login</TabsTrigger>
                                <TabsTrigger value="user">Staff Login</TabsTrigger>
                            </TabsList>
                        </CardHeader>

                        <CardContent className="space-y-4">
                            {/* Admin Login Tab */}
                            <TabsContent value="admin" className="mt-0">
                                <form onSubmit={(e) => { e.preventDefault(); handleAdminLogin(); }} className="space-y-4">
                                    <CardDescription>Sign in with your admin credentials</CardDescription>
                                    <div className="space-y-2">
                                        <Label htmlFor="admin-name">Username</Label>
                                        <Input
                                            id="admin-name"
                                            autoComplete="username"
                                            placeholder="Enter admin username"
                                            value={adminName}
                                            onChange={(e) => setAdminName(e.target.value)}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="admin-password">Password</Label>
                                        <Input
                                            id="admin-password"
                                            type="password"
                                            autoComplete="current-password"
                                            placeholder="Enter password"
                                            value={adminPassword}
                                            onChange={(e) => setAdminPassword(e.target.value)}
                                        />
                                    </div>
                                    <Button
                                        type="submit"
                                        className="w-full"
                                        disabled={isLoading}
                                    >
                                        {isLoading ? "Signing in..." : "Sign In"}
                                    </Button>
                                </form>
                            </TabsContent>

                            {/* User Login Tab */}
                            <TabsContent value="user" className="mt-0">
                                <form onSubmit={(e) => { e.preventDefault(); handleUserLogin(); }} className="space-y-4">
                                    <CardDescription>Sign in with your staff name and check code</CardDescription>
                                    <div className="space-y-2">
                                        <Label htmlFor="staff-name">Staff Name</Label>
                                        <Input
                                            id="staff-name"
                                            placeholder="Enter staff name"
                                            value={staffName}
                                            onChange={(e) => setStaffName(e.target.value)}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="check-code">Check Code</Label>
                                        <Input
                                            id="check-code"
                                            type="number"
                                            placeholder="Enter check code"
                                            value={checkCode}
                                            onChange={(e) => setCheckCode(e.target.value)}
                                        />
                                    </div>
                                    <Button
                                        type="submit"
                                        className="w-full"
                                        disabled={isLoading}
                                    >
                                        {isLoading ? "Signing in..." : "Sign In"}
                                    </Button>
                                </form>
                            </TabsContent>

                            {/* Register Link */}
                            <div className="text-center pt-2">
                                <Button
                                    variant="link"
                                    className="text-sm text-muted-foreground"
                                    onClick={() => router.push("/register")}
                                >
                                    Don&apos;t have an account? Register
                                </Button>
                            </div>
                        </CardContent>
                    </Tabs>
                </Card>
            </div>
        </div>
    );
}
