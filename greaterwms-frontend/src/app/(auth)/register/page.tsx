"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Boxes } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api-client";
import { toast } from "sonner";

export default function RegisterPage() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(false);
    const [name, setName] = useState("");
    const [password1, setPassword1] = useState("");
    const [password2, setPassword2] = useState("");

    const handleRegister = async () => {
        if (password1 !== password2) {
            toast.error("Passwords do not match");
            return;
        }
        if (!name || !password1) {
            toast.error("Please fill in all fields");
            return;
        }
        setIsLoading(true);
        try {
            await api.post("register/", { name, password1, password2 });
            toast.success("Registration successful! Please log in.");
            router.push("/login");
        } catch (err: unknown) {
            const error = err as { detail?: string };
            toast.error(error.detail || "Registration failed");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
            <div className="w-full max-w-md space-y-6">
                <div className="text-center space-y-2">
                    <div className="inline-flex items-center justify-center rounded-xl bg-primary/10 p-3">
                        <Boxes className="h-8 w-8 text-primary" />
                    </div>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-primary to-blue-400 bg-clip-text text-transparent">
                        GreaterWMS
                    </h1>
                    <p className="text-sm text-muted-foreground">Create your account</p>
                </div>

                <Card className="border-border/50 shadow-2xl">
                    <CardHeader>
                        <CardTitle>Register</CardTitle>
                        <CardDescription>Create a new warehouse account</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={(e) => { e.preventDefault(); handleRegister(); }} className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Username</Label>
                                <Input
                                    id="name"
                                    autoComplete="username"
                                    placeholder="Choose a username"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="password1">Password</Label>
                                <Input
                                    id="password1"
                                    type="password"
                                    autoComplete="new-password"
                                    placeholder="Choose a password"
                                    value={password1}
                                    onChange={(e) => setPassword1(e.target.value)}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="password2">Confirm Password</Label>
                                <Input
                                    id="password2"
                                    type="password"
                                    autoComplete="new-password"
                                    placeholder="Confirm your password"
                                    value={password2}
                                    onChange={(e) => setPassword2(e.target.value)}
                                />
                            </div>
                            <Button
                                type="submit"
                                className="w-full"
                                disabled={isLoading}
                            >
                                {isLoading ? "Creating account..." : "Create Account"}
                            </Button>
                        </form>
                        <div className="text-center pt-2">
                            <Button
                                variant="link"
                                className="text-sm text-muted-foreground"
                                onClick={() => router.push("/login")}
                            >
                                Already have an account? Sign in
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
