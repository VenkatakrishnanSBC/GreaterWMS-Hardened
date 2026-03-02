"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { BinSet } from "@/types/models";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

const columns: ColumnConfig<BinSet>[] = [
    { key: "bin_name", header: "Bin Name", accessor: (r) => <span className="font-mono font-medium">{r.bin_name}</span> },
    { key: "bin_size", header: "Size", accessor: (r) => r.bin_size, align: "center" },
    { key: "bin_property", header: "Property", accessor: (r) => <Badge variant="outline">{r.bin_property}</Badge>, align: "center" },
    { key: "empty_label", header: "Empty", accessor: (r) => <Badge variant={r.empty_label ? "default" : "secondary"}>{r.empty_label ? "Yes" : "No"}</Badge>, align: "center" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "bin_name", label: "Bin Name", placeholder: "A-01-01", required: true },
    { key: "bin_size", label: "Size", placeholder: "Large / Medium / Small", required: true },
    {
        key: "bin_property", label: "Property", type: "select", options: [
            { label: "Normal", value: "Normal" },
            { label: "Damage", value: "Damage" },
            { label: "Inspection", value: "Inspection" },
            { label: "Holding", value: "Holding" },
        ]
    },
];

export default function BinPage() {
    const crud = useCrud<BinSet>({ endpoint: "binset/list/", queryKey: "binset" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<BinSet | null>(null);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Bin Management</h1>
                <p className="text-muted-foreground">Configure storage bin locations</p>
            </div>
            <CrudTable
                title="Bin List"
                columns={columns}
                data={crud.data}
                totalCount={crud.totalCount}
                page={crud.page}
                totalPages={crud.totalPages}
                isLoading={crud.isLoading}
                onPageChange={crud.goToPage}
                onSearch={crud.setSearch}
                onRefresh={() => crud.refetch()}
                onCreate={() => { setEditItem(null); setDialogOpen(true); }}
                onEdit={(item) => { setEditItem(item); setDialogOpen(true); }}
                onDelete={(item) => crud.remove(item.id)}
                isDeleting={crud.isDeleting}
            />
            <CrudDialog
                open={dialogOpen}
                onClose={() => setDialogOpen(false)}
                title="Bin"
                description="Add or edit bin location"
                fields={formFields}
                initialData={editItem}
                isLoading={crud.isCreating || crud.isUpdating}
                onSubmit={async (data) => {
                    if (editItem) await crud.update(editItem.id, data as Partial<BinSet>);
                    else await crud.create(data as Partial<BinSet>);
                    setDialogOpen(false);
                }}
            />
        </div>
    );
}
