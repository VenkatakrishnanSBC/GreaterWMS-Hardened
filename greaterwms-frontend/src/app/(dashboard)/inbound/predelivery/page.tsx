"use client";
import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import { Badge } from "@/components/ui/badge";

interface StockRecord { id: number; asn_code: string; goods_code: string; goods_qty: number; goods_actual_qty: number; goods_weight: number; creater: string; create_time: string; update_time: string; }

const columns: ColumnConfig<StockRecord>[] = [
    { key: "asn_code", header: "ASN Code", accessor: (r) => <span className="font-mono">{r.asn_code}</span> },
    { key: "goods_code", header: "Goods Code", accessor: (r) => r.goods_code },
    { key: "goods_qty", header: "Expected Qty", accessor: (r) => r.goods_qty, align: "right" },
    { key: "goods_actual_qty", header: "Actual Qty", accessor: (r) => <Badge variant={r.goods_actual_qty > 0 ? "default" : "outline"}>{r.goods_actual_qty}</Badge>, align: "center" },
    { key: "goods_weight", header: "Weight", accessor: (r) => r.goods_weight.toFixed(2), align: "right" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
    { key: "create_time", header: "Created", accessor: (r) => new Date(r.create_time).toLocaleDateString() },
];

export default function PredeliveryPage() {
    const crud = useCrud<StockRecord>({ endpoint: "asn/predeliverystock/", queryKey: "predelivery" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Pre-Delivery Stock</h1><p className="text-muted-foreground">Stock awaiting delivery confirmation</p></div>
            <CrudTable title="Pre-Delivery" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} />
        </div>
    );
}
