"use client";

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { useState, useEffect, type ReactNode } from "react";

export interface FieldConfig {
    key: string;
    label: string;
    type?: "text" | "number" | "select" | "textarea";
    placeholder?: string;
    required?: boolean;
    options?: { label: string; value: string }[];
    disabled?: boolean;
}

interface CrudDialogProps<T> {
    open: boolean;
    onClose: () => void;
    onSubmit: (data: Record<string, unknown>) => void;
    fields: FieldConfig[];
    title: string;
    description?: string;
    initialData?: T | null;
    isLoading?: boolean;
    children?: ReactNode;
}

export function CrudDialog<T extends object>({
    open,
    onClose,
    onSubmit,
    fields,
    title,
    description,
    initialData,
    isLoading,
}: CrudDialogProps<T>) {
    const [formData, setFormData] = useState<Record<string, unknown>>({});
    const isEdit = !!initialData;

    useEffect(() => {
        if (initialData) {
            setFormData(initialData as Record<string, unknown>);
        } else {
            const defaults: Record<string, unknown> = {};
            fields.forEach((f) => {
                defaults[f.key] = f.type === "number" ? 0 : "";
            });
            setFormData(defaults);
        }
    }, [initialData, fields, open]);

    const handleChange = (key: string, value: unknown) => {
        setFormData((prev) => ({ ...prev, [key]: value }));
    };

    const handleSubmit = () => {
        onSubmit(formData);
    };

    return (
        <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
            <DialogContent className="sm:max-w-[500px] max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>{isEdit ? `Edit ${title}` : `New ${title}`}</DialogTitle>
                    {description && <DialogDescription>{description}</DialogDescription>}
                </DialogHeader>

                <div className="grid gap-4 py-4">
                    {fields.map((field) => (
                        <div key={field.key} className="grid gap-2">
                            <Label htmlFor={field.key}>
                                {field.label}
                                {field.required && <span className="text-destructive ml-1">*</span>}
                            </Label>

                            {field.type === "select" ? (
                                <Select
                                    value={String(formData[field.key] || "")}
                                    onValueChange={(v) => handleChange(field.key, v)}
                                    disabled={field.disabled}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder={field.placeholder || `Select ${field.label}`} />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {field.options?.map((opt) => (
                                            <SelectItem key={opt.value} value={opt.value}>
                                                {opt.label}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            ) : field.type === "textarea" ? (
                                <textarea
                                    id={field.key}
                                    className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                                    placeholder={field.placeholder}
                                    value={String(formData[field.key] || "")}
                                    onChange={(e) => handleChange(field.key, e.target.value)}
                                    disabled={field.disabled}
                                />
                            ) : (
                                <Input
                                    id={field.key}
                                    type={field.type || "text"}
                                    placeholder={field.placeholder}
                                    value={formData[field.key] !== undefined ? String(formData[field.key]) : ""}
                                    onChange={(e) =>
                                        handleChange(
                                            field.key,
                                            field.type === "number" ? Number(e.target.value) : e.target.value
                                        )
                                    }
                                    disabled={field.disabled}
                                />
                            )}
                        </div>
                    ))}
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={onClose}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} disabled={isLoading}>
                        {isLoading ? "Saving..." : isEdit ? "Update" : "Create"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
