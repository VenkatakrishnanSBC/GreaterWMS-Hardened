"use client";
import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";

interface StockRecord { id: number; asn_code: string; goods_code: string; goods_qty: number; goods_actual_qty: number; goods_weight: number; creater: string; create_time: string; update_time: string; }

const columns: ColumnConfig<StockRecord>[] = [
    { key: "asn_code", header: "ASN Code", accessor: (r) => <span className="font-mono">{r.asn_code}</span> },
    { key: "goods_code", header: "Goods Code", accessor: (r) => r.goods_code },
    { key: "goods_qty", header: "Qty", accessor: (r) => r.goods_qty, align: "right" },
    { key: "goods_actual_qty", header: "Actual Qty", accessor: (r) => r.goods_actual_qty, align: "right" },
    { key: "creater", header: "Creator", accessor: (r) => r.creater },
];

export default function PresortPage() {
    const crud = useCrud<StockRecord>({ endpoint: "asn/presortstock/", queryKey: "presort" });
    return (
        <div className="space-y-6">
            <div><h1 className="text-2xl font-bold">Pre-Sort Stock</h1><p className="text-muted-foreground">Stock awaiting sorting</p></div>
            <CrudTable title="Pre-Sort" columns={columns} data={crud.data} totalCount={crud.totalCount} page={crud.page} totalPages={crud.totalPages} isLoading={crud.isLoading} onPageChange={crud.goToPage} onSearch={crud.setSearch} onRefresh={() => crud.refetch()} />
        </div>
    );
}
