"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { Staff } from "@/types/models";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";

const columns: ColumnConfig<Staff>[] = [
    { key: "staff_name", header: "Name", accessor: (r) => <span className="font-semibold">{r.staff_name}</span> },
    { key: "staff_type", header: "Type", accessor: (r) => <Badge variant="outline">{r.staff_type}</Badge>, align: "center" },
    { key: "check_code", header: "Check Code", accessor: (r) => <span className="font-mono">{r.check_code}</span>, align: "center" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "staff_name", label: "Staff Name", placeholder: "Full name", required: true },
    {
        key: "staff_type", label: "Role", type: "select", required: true, options: [
            { label: "Admin", value: "Admin" },
            { label: "Inbound Manager", value: "Inbound" },
            { label: "Outbound Manager", value: "Outbound" },
            { label: "Warehouse Worker", value: "Worker" },
            { label: "Driver", value: "Driver" },
        ]
    },
    { key: "check_code", label: "Check Code", type: "number", placeholder: "4-digit code" },
];

export default function StaffListPage() {
    const crud = useCrud<Staff>({ endpoint: "staff/list/", queryKey: "staff" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Staff | null>(null);

    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Staff Management</h1><p className="text-muted-foreground">Manage staff and access</p></div>
            <CrudTable title="Staff List" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { setEditItem(null); setDialogOpen(true); }} onEdit={(item) => { setEditItem(item); setDialogOpen(true); }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
            <CrudDialog open={dialogOpen} onClose={() => setDialogOpen(false)} title="Staff Member" description="Add or edit staff" fields={formFields} initialData={editItem} isLoading={crud.isCreating || crud.isUpdating} onSubmit={async (data) => { if (editItem) await crud.update(editItem.id, data as Partial<Staff>); else await crud.create(data as Partial<Staff>); setDialogOpen(false); }} />
        </div>
    );
}
