"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { Warehouse } from "@/types/models";
import { useState } from "react";

const columns: ColumnConfig<Warehouse>[] = [
    { key: "warehouse_name", header: "Warehouse", accessor: (r) => <span className="font-semibold">{r.warehouse_name}</span> },
    { key: "warehouse_city", header: "City", accessor: (r) => r.warehouse_city },
    { key: "warehouse_address", header: "Address", accessor: (r) => r.warehouse_address },
    { key: "warehouse_contact", header: "Contact", accessor: (r) => r.warehouse_contact, align: "center" },
    { key: "warehouse_manager", header: "Manager", accessor: (r) => r.warehouse_manager },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "warehouse_name", label: "Warehouse Name", placeholder: "Main Warehouse", required: true },
    { key: "warehouse_city", label: "City", placeholder: "City" },
    { key: "warehouse_address", label: "Address", placeholder: "Full address" },
    { key: "warehouse_contact", label: "Contact", placeholder: "Phone number" },
    { key: "warehouse_manager", label: "Manager", placeholder: "Manager name" },
];

export default function WarehouseSettingsPage() {
    const crud = useCrud<Warehouse>({ endpoint: "warehouse/list/", queryKey: "warehouse" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Warehouse | null>(null);

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Warehouse Settings</h1>
                <p className="text-muted-foreground">Manage warehouse locations and configuration</p>
            </div>
            <CrudTable
                title="Warehouses"
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
                title="Warehouse"
                description="Add or edit warehouse details"
                fields={formFields}
                initialData={editItem}
                isLoading={crud.isCreating || crud.isUpdating}
                onSubmit={async (data) => {
                    if (editItem) await crud.update(editItem.id, data as Partial<Warehouse>);
                    else await crud.create(data as Partial<Warehouse>);
                    setDialogOpen(false);
                }}
            />
        </div>
    );
}
