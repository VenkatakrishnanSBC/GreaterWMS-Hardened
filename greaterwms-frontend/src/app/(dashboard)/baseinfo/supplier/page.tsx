"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import type { Supplier } from "@/types/models";

const columns: ColumnConfig<Supplier>[] = [
    { key: "supplier_name", header: "Supplier", accessor: (r) => r.supplier_name },
    { key: "supplier_city", header: "City", accessor: (r) => r.supplier_city },
    { key: "supplier_address", header: "Address", accessor: (r) => r.supplier_address },
    { key: "supplier_contact", header: "Contact", accessor: (r) => r.supplier_contact, align: "center" },
    { key: "supplier_manager", header: "Manager", accessor: (r) => r.supplier_manager },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

export default function SupplierPage() {
    const crud = useCrud<Supplier>({ endpoint: "supplier/list/", queryKey: "supplier" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Suppliers</h1><p className="text-muted-foreground">Manage supplier directory</p></div>
            <CrudTable title="Supplier List" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { }} onEdit={() => { }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
        </div>
    );
}
