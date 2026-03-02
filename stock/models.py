from django.db import models


class StockListModel(models.Model):
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    # DB-005: ForeignKey to Goods model
    goods_fk = models.ForeignKey(
        'goods.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='stock_entries',
        verbose_name="Goods Reference"
    )
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    goods_qty = models.BigIntegerField(default=0, verbose_name="Total Qty")
    onhand_stock = models.BigIntegerField(default=0, verbose_name='On Hand Stock')
    can_order_stock = models.BigIntegerField(default=0, verbose_name='Can Order Stock')
    ordered_stock = models.BigIntegerField(default=0, verbose_name='Ordered Stock')
    inspect_stock = models.BigIntegerField(default=0, verbose_name='Inspect Stock')
    hold_stock = models.BigIntegerField(default=0, verbose_name='Holding Stock')
    damage_stock = models.BigIntegerField(default=0, verbose_name='Damage Stock')
    asn_stock = models.BigIntegerField(default=0, verbose_name='ASN Stock')
    dn_stock = models.BigIntegerField(default=0, verbose_name='DN Stock')
    pre_load_stock = models.BigIntegerField(default=0, verbose_name='Pre Load Stock')
    pre_sort_stock = models.BigIntegerField(default=0, verbose_name='Pre Sort Stock')
    sorted_stock = models.BigIntegerField(default=0, verbose_name='Sorted Stock')
    pick_stock = models.BigIntegerField(default=0, verbose_name='Pick Stock')
    picked_stock = models.BigIntegerField(default=0, verbose_name='Picked Stock')
    back_order_stock = models.BigIntegerField(default=0, verbose_name='Back Order Stock')
    supplier = models.CharField(default='', max_length=255, verbose_name='Goods Supplier')
    # DB-005: ForeignKey to Supplier model
    supplier_fk = models.ForeignKey(
        'supplier.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='stock_entries',
        verbose_name="Supplier Reference"
    )
    openid = models.CharField(max_length=255, verbose_name="Openid")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'stocklist'
        verbose_name = 'Stock List'
        verbose_name_plural = "Stock List"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes for query performance
        indexes = [
            models.Index(fields=['openid'], name='idx_stocklist_openid'),
            models.Index(fields=['goods_code'], name='idx_stocklist_goods_code'),
            models.Index(fields=['openid', 'goods_code'], name='idx_stocklist_oid_gc'),
        ]


class StockBinModel(models.Model):
    bin_name = models.CharField(max_length=255, verbose_name="Bin Name")
    # DB-005: ForeignKey to BinSet model
    bin_fk = models.ForeignKey(
        'binset.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='stock_binstock',
        verbose_name="Bin Reference"
    )
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    # DB-005: ForeignKey to Goods model
    goods_fk = models.ForeignKey(
        'goods.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='stock_binstock',
        verbose_name="Goods Reference"
    )
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    goods_qty = models.BigIntegerField(default=0, verbose_name="Binstock Qty")
    pick_qty = models.BigIntegerField(default=0, verbose_name="BinPick Qty")
    picked_qty = models.BigIntegerField(default=0, verbose_name="BinPicked Qty")
    bin_size = models.CharField(max_length=255, verbose_name="Bin size")
    bin_property = models.CharField(max_length=255, verbose_name="Bin Property")
    t_code = models.CharField(max_length=255, verbose_name="Transaction Code")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")  # DB-007 / ISS-029: Fixed auto_now_add=False → True
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'stockbin'
        verbose_name = 'Stock Bin'
        verbose_name_plural = "Stock Bin"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid'], name='idx_stockbin_openid'),
            models.Index(fields=['bin_name'], name='idx_stockbin_bin_name'),
            models.Index(fields=['goods_code'], name='idx_stockbin_goods_code'),
            models.Index(fields=['openid', 'bin_name'], name='idx_stockbin_oid_bn'),
        ]
