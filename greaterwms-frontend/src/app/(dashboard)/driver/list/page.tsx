"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import type { Driver } from "@/types/models";

const columns: ColumnConfig<Driver>[] = [
    { key: "driver_name", header: "Name", accessor: (r) => r.driver_name },
    { key: "license_plate", header: "License Plate", accessor: (r) => r.license_plate, align: "center" },
    { key: "contact", header: "Contact", accessor: (r) => r.contact, align: "center" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

export default function DriverListPage() {
    const crud = useCrud<Driver>({ endpoint: "driver/list/", queryKey: "driver" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Drivers</h1><p className="text-muted-foreground">Manage driver fleet</p></div>
            <CrudTable title="Driver List" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { }} onEdit={() => { }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
        </div>
    );
}
