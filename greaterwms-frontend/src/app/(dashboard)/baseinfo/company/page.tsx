"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { CrudDialog, type FieldConfig } from "@/components/forms/crud-dialog";
import { useCrud } from "@/hooks/use-crud";
import type { Company } from "@/types/models";
import { useState } from "react";

const columns: ColumnConfig<Company>[] = [
    { key: "company_name", header: "Company", accessor: (r) => <span className="font-semibold">{r.company_name}</span> },
    { key: "company_city", header: "City", accessor: (r) => r.company_city },
    { key: "company_address", header: "Address", accessor: (r) => r.company_address },
    { key: "company_contact", header: "Contact", accessor: (r) => r.company_contact, align: "center" },
    { key: "company_manager", header: "Manager", accessor: (r) => r.company_manager },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

const formFields: FieldConfig[] = [
    { key: "company_name", label: "Company Name", placeholder: "Enter company name", required: true },
    { key: "company_city", label: "City", placeholder: "City" },
    { key: "company_address", label: "Address", type: "textarea", placeholder: "Full address" },
    { key: "company_contact", label: "Contact", placeholder: "Phone or email" },
    { key: "company_manager", label: "Manager", placeholder: "Manager name" },
];

export default function CompanyPage() {
    const crud = useCrud<Company>({ endpoint: "company/list/", queryKey: "company" });
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Company | null>(null);

    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Company Info</h1><p className="text-muted-foreground">Manage company details</p></div>
            <CrudTable title="Companies" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { setEditItem(null); setDialogOpen(true); }} onEdit={(item) => { setEditItem(item); setDialogOpen(true); }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
            <CrudDialog open={dialogOpen} onClose={() => setDialogOpen(false)} title="Company" description="Add or edit company" fields={formFields} initialData={editItem} isLoading={crud.isCreating || crud.isUpdating} onSubmit={async (data) => { if (editItem) await crud.update(editItem.id, data as Partial<Company>); else await crud.create(data as Partial<Company>); setDialogOpen(false); }} />
        </div>
    );
}
