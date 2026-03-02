"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { DN } from "@/types/models";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

const statusMap: Record<number, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
    1: { label: "New", variant: "outline" },
    2: { label: "Picked", variant: "secondary" },
    3: { label: "Packed", variant: "secondary" },
    4: { label: "Shipped", variant: "default" },
    5: { label: "Back Order", variant: "destructive" },
    6: { label: "POD", variant: "default" },
};

const columns: ColumnConfig<DN>[] = [
    { key: "dn_code", header: "DN Code", accessor: (r) => <span className="font-mono font-medium">{r.dn_code}</span> },
    {
        key: "dn_status", header: "Status",
        accessor: (r) => {
            const s = statusMap[r.dn_status] || { label: String(r.dn_status), variant: "outline" as const };
            return <Badge variant={s.variant}>{s.label}</Badge>;
        },
        align: "center",
    },
    { key: "total_weight", header: "Weight", accessor: (r) => r.total_weight.toFixed(2), align: "right" },
    { key: "total_volume", header: "Volume", accessor: (r) => r.total_volume.toFixed(2), align: "right" },
    { key: "customer", header: "Customer", accessor: (r) => r.customer },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "customer", label: "Customer", placeholder: "Enter customer name", required: true },
    { key: "goods_code", label: "Goods Code", placeholder: "Enter goods code" },
    { key: "goods_qty", label: "Quantity", type: "number", placeholder: "0" },
];

export default function DNPage() {
    const crud = useCrud<DN>({ endpoint: "dn/list/", queryKey: "dn" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<DN | null>(null);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Outbound — Delivery Notice</h1>
                <p className="text-muted-foreground">Manage Delivery Notices and shipments</p>
            </div>
            <CrudTable
                title="DN List"
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
                title="Delivery Notice"
                fields={formFields}
                initialData={editItem}
                isLoading={crud.isCreating || crud.isUpdating}
                onSubmit={async (data) => {
                    if (editItem) await crud.update(editItem.id, data as Partial<DN>);
                    else await crud.create(data as Partial<DN>);
                    setDialogOpen(false);
                }}
            />
        </div>
    );
}
