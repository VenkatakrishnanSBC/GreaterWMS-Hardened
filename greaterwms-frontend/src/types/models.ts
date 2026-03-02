// ===== Warehouse =====
export interface Warehouse {
    id: number;
    warehouse_name: string;
    warehouse_city: string;
    warehouse_address: string;
    warehouse_contact: string;
    warehouse_manager: string;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Goods =====
export interface Goods {
    id: number;
    goods_code: string;
    goods_desc: string;
    goods_supplier: string;
    goods_weight: number;
    goods_w: number;
    goods_d: number;
    goods_h: number;
    goods_volume: number;
    goods_unit: string;
    goods_class: string;
    goods_brand: string;
    goods_color: string;
    goods_shape: string;
    goods_specs: string;
    goods_origin: string;
    goods_cost: number;
    goods_price: number;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Inbound (ASN) =====
export interface ASN {
    id: number;
    asn_code: string;
    asn_status: number;
    total_weight: number;
    total_volume: number;
    total_cost: number;
    supplier: string;
    creater: string;
    create_time: string;
    update_time: string;
    transportation_fee: {
        detail: Array<{
            transportation_supplier: string;
            transportation_cost: number;
        }>;
    };
}

// ===== Outbound (DN) =====
export interface DN {
    id: number;
    dn_code: string;
    dn_status: number;
    total_weight: number;
    total_volume: number;
    total_cost: number;
    customer: string;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Stock =====
export interface Stock {
    id: number;
    goods_code: string;
    goods_desc: string;
    goods_qty: number;
    onhand_stock: number;
    can_order_stock: number;
    ordered_stock: number;
    inspect_stock: number;
    hold_stock: number;
    damage_stock: number;
    asn_stock: number;
    dn_stock: number;
    pre_load_stock: number;
    pre_sort_stock: number;
    sorted_stock: number;
    pick_stock: number;
    picked_stock: number;
    back_order_stock: number;
    bin_name: string;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Base Info =====
export interface Company {
    id: number;
    company_name: string;
    company_city: string;
    company_address: string;
    company_contact: string;
    company_manager: string;
    creater: string;
    create_time: string;
    update_time: string;
}

export interface Supplier {
    id: number;
    supplier_name: string;
    supplier_city: string;
    supplier_address: string;
    supplier_contact: string;
    supplier_manager: string;
    creater: string;
    create_time: string;
    update_time: string;
}

export interface Customer {
    id: number;
    customer_name: string;
    customer_city: string;
    customer_address: string;
    customer_contact: string;
    customer_manager: string;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Staff =====
export interface Staff {
    id: number;
    staff_name: string;
    staff_type: string;
    check_code: number;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Driver =====
export interface Driver {
    id: number;
    driver_name: string;
    license_plate: string;
    contact: string;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Finance =====
export interface Capital {
    id: number;
    capital_name: string;
    capital_qty: number;
    capital_cost: number;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Bin =====
export interface BinSet {
    id: number;
    bin_name: string;
    bin_size: string;
    bin_property: string;
    empty_label: boolean;
    creater: string;
    create_time: string;
    update_time: string;
}

// ===== Lookup Tables =====
export interface LookupItem {
    id: number;
    name: string;
    creater: string;
    create_time: string;
    update_time: string;
}

export type GoodsUnit = LookupItem;
export type GoodsClass = LookupItem;
export type GoodsBrand = LookupItem;
export type GoodsColor = LookupItem;
export type GoodsShape = LookupItem;
export type GoodsSpecs = LookupItem;
export type GoodsOrigin = LookupItem;
