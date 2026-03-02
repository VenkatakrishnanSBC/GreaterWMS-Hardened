"use client";

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import {
    ChevronLeft,
    ChevronRight,
    ChevronsLeft,
    ChevronsRight,
    Plus,
    RefreshCw,
    Search,
    Pencil,
    Trash2,
} from "lucide-react";
import { useState, type ReactNode } from "react";

export interface ColumnConfig<T> {
    key: string;
    header: string;
    accessor: (row: T) => ReactNode;
    align?: "left" | "center" | "right";
}

interface CrudTableProps<T extends { id: number }> {
    title: string;
    columns: ColumnConfig<T>[];
    data: T[];
    totalCount: number;
    page: number;
    totalPages: number;
    isLoading: boolean;
    onPageChange: (page: number) => void;
    onSearch?: (query: string) => void;
    onRefresh: () => void;
    onDelete?: (item: T) => void;
    onEdit?: (item: T) => void;
    onCreate?: () => void;
    renderCreateForm?: () => ReactNode;
    renderEditForm?: (item: T) => ReactNode;
    isDeleting?: boolean;
}

export function CrudTable<T extends { id: number }>({
    title,
    columns,
    data,
    totalCount,
    page,
    totalPages,
    isLoading,
    onPageChange,
    onSearch,
    onRefresh,
    onDelete,
    onEdit,
    onCreate,
    isDeleting,
}: CrudTableProps<T>) {
    const [searchQuery, setSearchQuery] = useState("");
    const [deleteItem, setDeleteItem] = useState<T | null>(null);

    return (
        <div className="space-y-4">
            {/* Toolbar */}
            <div className="flex items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                    <h2 className="text-xl font-semibold">{title}</h2>
                    <span className="text-sm text-muted-foreground">
                        ({totalCount} records)
                    </span>
                </div>
                <div className="flex items-center gap-2">
                    {onSearch && (
                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search..."
                                className="pl-8 w-64"
                                value={searchQuery}
                                onChange={(e) => {
                                    setSearchQuery(e.target.value);
                                    onSearch(e.target.value);
                                }}
                            />
                        </div>
                    )}
                    <Button variant="outline" size="icon" onClick={onRefresh}>
                        <RefreshCw className="h-4 w-4" />
                    </Button>
                    {onCreate && (
                        <Button onClick={onCreate} size="sm">
                            <Plus className="h-4 w-4 mr-1" /> New
                        </Button>
                    )}
                </div>
            </div>

            {/* Table */}
            <div className="rounded-lg border bg-card">
                <Table>
                    <TableHeader>
                        <TableRow className="hover:bg-transparent">
                            {columns.map((col) => (
                                <TableHead
                                    key={col.key}
                                    className={
                                        col.align === "right"
                                            ? "text-right"
                                            : col.align === "center"
                                                ? "text-center"
                                                : ""
                                    }
                                >
                                    {col.header}
                                </TableHead>
                            ))}
                            {(onEdit || onDelete) && (
                                <TableHead className="text-right w-[100px]">Actions</TableHead>
                            )}
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {isLoading
                            ? Array.from({ length: 5 }).map((_, i) => (
                                <TableRow key={i}>
                                    {columns.map((col) => (
                                        <TableCell key={col.key}>
                                            <Skeleton className="h-4 w-full" />
                                        </TableCell>
                                    ))}
                                    {(onEdit || onDelete) && (
                                        <TableCell>
                                            <Skeleton className="h-4 w-16 ml-auto" />
                                        </TableCell>
                                    )}
                                </TableRow>
                            ))
                            : data.map((row) => (
                                <TableRow key={row.id}>
                                    {columns.map((col) => (
                                        <TableCell
                                            key={col.key}
                                            className={
                                                col.align === "right"
                                                    ? "text-right"
                                                    : col.align === "center"
                                                        ? "text-center"
                                                        : ""
                                            }
                                        >
                                            {col.accessor(row)}
                                        </TableCell>
                                    ))}
                                    {(onEdit || onDelete) && (
                                        <TableCell className="text-right">
                                            <div className="flex justify-end gap-1">
                                                {onEdit && (
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="h-8 w-8"
                                                        onClick={() => onEdit(row)}
                                                    >
                                                        <Pencil className="h-3.5 w-3.5" />
                                                    </Button>
                                                )}
                                                {onDelete && (
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        className="h-8 w-8 text-destructive hover:text-destructive"
                                                        onClick={() => setDeleteItem(row)}
                                                    >
                                                        <Trash2 className="h-3.5 w-3.5" />
                                                    </Button>
                                                )}
                                            </div>
                                        </TableCell>
                                    )}
                                </TableRow>
                            ))}
                        {!isLoading && data.length === 0 && (
                            <TableRow>
                                <TableCell
                                    colSpan={columns.length + (onEdit || onDelete ? 1 : 0)}
                                    className="text-center py-10 text-muted-foreground"
                                >
                                    No data available
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </div>

            {/* Pagination */}
            {totalPages > 0 && (
                <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                        Page {page} of {totalPages} • {totalCount} total
                    </p>
                    <div className="flex items-center gap-1">
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => onPageChange(1)}
                            disabled={page <= 1}
                        >
                            <ChevronsLeft className="h-4 w-4" />
                        </Button>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => onPageChange(page - 1)}
                            disabled={page <= 1}
                        >
                            <ChevronLeft className="h-4 w-4" />
                        </Button>
                        <span className="px-3 text-sm font-medium">{page}</span>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => onPageChange(page + 1)}
                            disabled={page >= totalPages}
                        >
                            <ChevronRight className="h-4 w-4" />
                        </Button>
                        <Button
                            variant="outline"
                            size="icon"
                            className="h-8 w-8"
                            onClick={() => onPageChange(totalPages)}
                            disabled={page >= totalPages}
                        >
                            <ChevronsRight className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            )}

            {/* Delete Confirmation Dialog */}
            <Dialog open={!!deleteItem} onOpenChange={() => setDeleteItem(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Confirm Deletion</DialogTitle>
                        <DialogDescription>
                            Are you sure you want to delete this record? This action cannot be
                            undone.
                        </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setDeleteItem(null)}>
                            Cancel
                        </Button>
                        <Button
                            variant="destructive"
                            disabled={isDeleting}
                            onClick={() => {
                                if (deleteItem && onDelete) {
                                    onDelete(deleteItem);
                                    setDeleteItem(null);
                                }
                            }}
                        >
                            {isDeleting ? "Deleting..." : "Delete"}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
}
