"use client";
import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import { Badge } from "@/components/ui/badge";

interface StockRecord { id: number; dn_code: string; goods_code: string; goods_qty: number; shipped_qty: number; customer: string; creater: string; create_time: string; update_time: string; }

const columns: ColumnConfig<StockRecord>[] = [
    { key: "dn_code", header: "DN Code", accessor: (r) => <span className="font-mono">{r.dn_code}</span> },
    { key: "goods_code", header: "Goods Code", accessor: (r) => r.goods_code },
    { key: "goods_qty", header: "Order Qty", accessor: (r) => r.goods_qty, align: "right" },
    { key: "shipped_qty", header: "Shipped", accessor: (r) => <Badge variant="default">{r.shipped_qty}</Badge>, align: "center" },
    { key: "customer", header: "Customer", accessor: (r) => r.customer },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
];

export default function ShippedPage() {
    const crud = useCrud<StockRecord>({ endpoint: "dn/shippedstock/", queryKey: "shipped" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Shipped Stock</h1><p className="text-muted-foreground">Completed shipments</p></div>
            <CrudTable title="Shipped" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} />
        </div>
    );
}
