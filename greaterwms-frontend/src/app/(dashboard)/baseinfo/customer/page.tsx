"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import type { Customer } from "@/types/models";

const columns: ColumnConfig<Customer>[] = [
    { key: "customer_name", header: "Customer", accessor: (r) => r.customer_name },
    { key: "customer_city", header: "City", accessor: (r) => r.customer_city },
    { key: "customer_address", header: "Address", accessor: (r) => r.customer_address },
    { key: "customer_contact", header: "Contact", accessor: (r) => r.customer_contact, align: "center" },
    { key: "customer_manager", header: "Manager", accessor: (r) => r.customer_manager },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

export default function CustomerPage() {
    const crud = useCrud<Customer>({ endpoint: "customer/list/", queryKey: "customer" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Customers</h1><p className="text-muted-foreground">Manage customer directory</p></div>
            <CrudTable title="Customer List" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { }} onEdit={() => { }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
        </div>
    );
}
