"use client";

import { CrudTable, type ColumnConfig } from "@/components/data-table/crud-table";
import { useCrud } from "@/hooks/use-crud";
import type { Stock } from "@/types/models";
import { Badge } from "@/components/ui/badge";

const columns: ColumnConfig<Stock>[] = [
    { key: "goods_code", header: "Product Code", accessor: (r) => r.goods_code },
    { key: "goods_desc", header: "Description", accessor: (r) => r.goods_desc },
    { key: "bin_name", header: "Bin", accessor: (r) => r.bin_name, align: "center" },
    {
        key: "goods_qty",
        header: "Total Qty",
        accessor: (r) => (
            <Badge variant={r.goods_qty > 0 ? "default" : "destructive"}>
                {r.goods_qty}
            </Badge>
        ),
        align: "center",
    },
    { key: "onhand_stock", header: "On Hand", accessor: (r) => r.onhand_stock, align: "right" },
    { key: "can_order_stock", header: "Available", accessor: (r) => r.can_order_stock, align: "right" },
    { key: "ordered_stock", header: "Ordered", accessor: (r) => r.ordered_stock, align: "right" },
    { key: "asn_stock", header: "ASN", accessor: (r) => r.asn_stock, align: "right" },
    { key: "dn_stock", header: "DN", accessor: (r) => r.dn_stock, align: "right" },
    { key: "pick_stock", header: "Pick", accessor: (r) => r.pick_stock, align: "right" },
];

export default function StockListPage() {
    const crud = useCrud<Stock>({ endpoint: "stock/list/", queryKey: "stock" });

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold">Stock Overview</h1>
                <p className="text-muted-foreground">Real-time inventory levels</p>
            </div>
            <CrudTable
                title="Stock List"
                columns={columns}
                data={crud.data}
                totalCount={crud.totalCount}
                page={crud.page}
                totalPages={crud.totalPages}
                isLoading={crud.isLoading}
                onPageChange={crud.goToPage}
                onSearch={crud.setSearch}
                onRefresh={() => crud.refetch()}
            />
        </div>
    );
}
