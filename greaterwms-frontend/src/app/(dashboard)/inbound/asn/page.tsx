"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { ASN } from "@/types/models";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

const statusMap: Record<number, { label: string; variant: "default" | "secondary" | "destructive" | "outline" }> = {
    1: { label: "Pre-Delivery", variant: "outline" },
    2: { label: "Pre-Load", variant: "secondary" },
    3: { label: "Pre-Sort", variant: "secondary" },
    4: { label: "Sorted", variant: "default" },
    5: { label: "Shortage", variant: "destructive" },
    6: { label: "Finished", variant: "default" },
};

const columns: ColumnConfig<ASN>[] = [
    { key: "asn_code", header: "ASN Code", accessor: (r) => <span className="font-mono font-medium">{r.asn_code}</span> },
    {
        key: "asn_status",
        header: "Status",
        accessor: (r) => {
            const s = statusMap[r.asn_status] || { label: String(r.asn_status), variant: "outline" as const };
            return <Badge variant={s.variant}>{s.label}</Badge>;
        },
        align: "center",
    },
    { key: "total_weight", header: "Weight", accessor: (r) => r.total_weight.toFixed(2), align: "right" },
    { key: "total_volume", header: "Volume", accessor: (r) => r.total_volume.toFixed(2), align: "right" },
    { key: "supplier", header: "Supplier", accessor: (r) => r.supplier },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "supplier", label: "Supplier", placeholder: "Enter supplier name", required: true },
    { key: "goods_code", label: "Goods Code", placeholder: "Enter goods code" },
    { key: "goods_qty", label: "Quantity", type: "number", placeholder: "0" },
];

export default function ASNPage() {
    const crud = useCrud<ASN>({ endpoint: "asn/list/", queryKey: "asn" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<ASN | null>(null);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Inbound — ASN</h1>
                <p className="text-muted-foreground">Manage Advanced Shipping Notices</p>
            </div>
            <CrudTable
                title="ASN List"
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
                title="ASN"
                description="Create or edit an Advanced Shipping Notice"
                fields={formFields}
                initialData={editItem}
                isLoading={crud.isCreating || crud.isUpdating}
                onSubmit={async (data) => {
                    if (editItem) {
                        await crud.update(editItem.id, data as Partial<ASN>);
                    } else {
                        await crud.create(data as Partial<ASN>);
                    }
                    setDialogOpen(false);
                }}
            />
        </div>
    );
}
