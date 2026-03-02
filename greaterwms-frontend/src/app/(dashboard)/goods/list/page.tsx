"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { Goods } from "@/types/models";
import { useState } from "react";

const columns: ColumnConfig<Goods>[] = [
    { key: "goods_code", header: "Code", accessor: (r) => <span className="font-mono font-medium">{r.goods_code}</span> },
    { key: "goods_desc", header: "Description", accessor: (r) => r.goods_desc },
    { key: "goods_supplier", header: "Supplier", accessor: (r) => r.goods_supplier },
    { key: "goods_unit", header: "Unit", accessor: (r) => r.goods_unit, align: "center" },
    { key: "goods_class", header: "Class", accessor: (r) => r.goods_class, align: "center" },
    { key: "goods_brand", header: "Brand", accessor: (r) => r.goods_brand, align: "center" },
    { key: "goods_weight", header: "Weight", accessor: (r) => r.goods_weight, align: "right" },
    { key: "goods_cost", header: "Cost", accessor: (r) => `$${r.goods_cost.toFixed(2)}`, align: "right" },
    { key: "goods_price", header: "Price", accessor: (r) => `$${r.goods_price.toFixed(2)}`, align: "right" },
];

const formFields: FieldConfig[] = [
    { key: "goods_code", label: "Product Code", placeholder: "SKU-001", required: true },
    { key: "goods_desc", label: "Description", type: "textarea", placeholder: "Product description" },
    { key: "goods_supplier", label: "Supplier", placeholder: "Supplier name" },
    { key: "goods_weight", label: "Weight (kg)", type: "number", placeholder: "0" },
    { key: "goods_w", label: "Width (cm)", type: "number", placeholder: "0" },
    { key: "goods_d", label: "Depth (cm)", type: "number", placeholder: "0" },
    { key: "goods_h", label: "Height (cm)", type: "number", placeholder: "0" },
    { key: "goods_cost", label: "Cost ($)", type: "number", placeholder: "0.00" },
    { key: "goods_price", label: "Price ($)", type: "number", placeholder: "0.00" },
];

export default function GoodsListPage() {
    const crud = useCrud<Goods>({ endpoint: "goods/list/", queryKey: "goods" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Goods | null>(null);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Goods Master</h1>
                <p className="text-muted-foreground">Manage product catalog</p>
            </div>
            <CrudTable
                title="Goods List"
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
                title="Product"
                description="Add or edit product details"
                fields={formFields}
                initialData={editItem}
                isLoading={crud.isCreating || crud.isUpdating}
                onSubmit={async (data) => {
                    if (editItem) await crud.update(editItem.id, data as Partial<Goods>);
                    else await crud.create(data as Partial<Goods>);
                    setDialogOpen(false);
                }}
            />
        </div>
    );
}
