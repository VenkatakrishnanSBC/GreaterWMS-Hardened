"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowUpFromLine, FolderUp } from "lucide-react";

export default function UploadPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Upload Center</h1>
                <p className="text-muted-foreground">
                    Import data via Excel files
                </p>
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {[
                    { title: "Initialize Upload", desc: "Upload initialization data for warehouse setup" },
                    { title: "Add Upload", desc: "Upload additional records to existing data" },
                ].map((item) => (
                    <Card key={item.title} className="hover:border-primary/50 transition-colors">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-lg">
                                <FolderUp className="h-5 w-5 text-primary" />
                                {item.title}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <p className="text-sm text-muted-foreground">{item.desc}</p>
                            <Button className="w-full">
                                <ArrowUpFromLine className="h-4 w-4 mr-2" /> Upload File
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
