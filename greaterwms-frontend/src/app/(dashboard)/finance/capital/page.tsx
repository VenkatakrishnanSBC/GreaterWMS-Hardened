"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import type { Capital } from "@/types/models";

const columns: ColumnConfig<Capital>[] = [
    { key: "capital_name", header: "Name", accessor: (r) => r.capital_name },
    { key: "capital_qty", header: "Quantity", accessor: (r) => r.capital_qty, align: "right" },
    { key: "capital_cost", header: "Cost", accessor: (r) => `$${r.capital_cost.toFixed(2)}`, align: "right" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

export default function CapitalPage() {
    const crud = useCrud<Capital>({ endpoint: "capital/list/", queryKey: "capital" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Finance — Capital</h1><p className="text-muted-foreground">Track capital and expenses</p></div>
            <CrudTable title="Capital List" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} onCreate={() => { }} onEdit={() => { }} onDelete={(item) => crud.remove(item.id)} isDeleting={crud.isDeleting} />
        </div>
    );
}
