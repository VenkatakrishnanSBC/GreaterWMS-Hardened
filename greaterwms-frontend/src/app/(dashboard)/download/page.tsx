"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download as DownloadIcon, FileDown } from "lucide-react";

const downloadTypes = [
    { title: "Inbound Data", endpoint: "downloadcenter/inbound/", desc: "Export inbound/ASN records" },
    { title: "Outbound Data", endpoint: "downloadcenter/outbound/", desc: "Export outbound/DN records" },
    { title: "Stock List", endpoint: "downloadcenter/stocklist/", desc: "Export current stock levels" },
    { title: "Goods List", endpoint: "downloadcenter/goodslist/", desc: "Export product catalog" },
    { title: "Bin List", endpoint: "downloadcenter/binlist/", desc: "Export bin configuration" },
];

export default function DownloadPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Download Center</h1>
                <p className="text-muted-foreground">Export data as Excel files</p>
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {downloadTypes.map((item) => (
                    <Card key={item.title} className="hover:border-primary/50 transition-colors">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-lg">
                                <FileDown className="h-5 w-5 text-primary" />
                                {item.title}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <p className="text-sm text-muted-foreground">{item.desc}</p>
                            <Button variant="outline" className="w-full">
                                <DownloadIcon className="h-4 w-4 mr-2" /> Export Excel
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
