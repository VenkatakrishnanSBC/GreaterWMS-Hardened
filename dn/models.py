from django.db import models

class DnListModel(models.Model):
    dn_code = models.CharField(max_length=255, verbose_name="DN Code")
    dn_status = models.BigIntegerField(default=1, verbose_name="DN Status")
    total_weight = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Total Weight")   # DB-003 / ISS-011
    total_volume = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Total Volume")   # DB-003 / ISS-011
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Cost")       # DB-003 / ISS-011
    customer = models.CharField(max_length=255, verbose_name="DN Customer")
    # DB-005: ForeignKey to Customer model (nullable for backward compatibility)
    customer_fk = models.ForeignKey(
        'customer.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='dn_orders',
        verbose_name="Customer Reference", db_column='customer_fk_id'
    )
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    bar_code = models.CharField(max_length=255, verbose_name="Bar Code")
    back_order_label = models.BooleanField(default=False, verbose_name='Back Order Label')
    openid = models.CharField(max_length=255, verbose_name="Openid")
    transportation_fee = models.JSONField(default=dict, verbose_name="Transportation Fee")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'dnlist'
        verbose_name = 'DN List'
        verbose_name_plural = "DN List"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_dnlist_oid_del'),
            models.Index(fields=['dn_code'], name='idx_dnlist_dn_code'),
            models.Index(fields=['openid', 'dn_status'], name='idx_dnlist_oid_status'),
        ]

class DnDetailModel(models.Model):
    dn_code = models.CharField(max_length=255, verbose_name="DN Code")
    # DB-005: ForeignKey to parent DN list
    dn_list = models.ForeignKey(
        DnListModel, on_delete=models.CASCADE,
        null=True, blank=True, related_name='details',
        verbose_name="DN List Reference"
    )
    dn_status = models.BigIntegerField(default=1, verbose_name="DN Status")
    customer = models.CharField(max_length=255, verbose_name="DN Customer")
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    # DB-005: ForeignKey to Goods model
    goods_fk = models.ForeignKey(
        'goods.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='dn_details',
        verbose_name="Goods Reference"
    )
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    goods_qty = models.BigIntegerField(default=0, verbose_name="Goods QTY")
    pick_qty = models.BigIntegerField(default=0, verbose_name="Goods Pre Pick QTY")
    picked_qty = models.BigIntegerField(default=0, verbose_name="Goods Picked QTY")
    intransit_qty = models.BigIntegerField(default=0, verbose_name="Intransit QTY")
    delivery_actual_qty = models.BigIntegerField(default=0, verbose_name="Delivery Actual QTY")
    delivery_shortage_qty = models.BigIntegerField(default=0, verbose_name="Delivery Shortage QTY")
    delivery_more_qty = models.BigIntegerField(default=0, verbose_name="Delivery More QTY")
    delivery_damage_qty = models.BigIntegerField(default=0, verbose_name="Delivery Damage QTY")  # CODE-006 / ISS-034: Fixed wrong verbose_name
    goods_weight = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Goods Weight")   # DB-003 / ISS-011
    goods_volume = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Goods Volume")   # DB-003 / ISS-011
    goods_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Goods Cost")       # DB-003 / ISS-011
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    back_order_label = models.BooleanField(default=False, verbose_name='Back Order Label')
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'dndetail'
        verbose_name = 'DN Detail'
        verbose_name_plural = "DN Detail"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_dndetail_oid_del'),
            models.Index(fields=['dn_code'], name='idx_dndetail_dn_code'),
            models.Index(fields=['goods_code'], name='idx_dndetail_gc'),
        ]

class PickingListModel(models.Model):
    dn_code = models.CharField(max_length=255, verbose_name="DN Code")
    # DB-005: ForeignKey to DN detail
    dn_detail = models.ForeignKey(
        DnDetailModel, on_delete=models.CASCADE,
        null=True, blank=True, related_name='picking_items',
        verbose_name="DN Detail Reference"
    )
    bin_name = models.CharField(max_length=255, verbose_name="Bin Name")
    # DB-005: ForeignKey to BinSet
    bin_fk = models.ForeignKey(
        'binset.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='picking_items',
        verbose_name="Bin Reference"
    )
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    # DB-005: ForeignKey to Goods
    goods_fk = models.ForeignKey(
        'goods.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='picking_items',
        verbose_name="Goods Reference"
    )
    picking_status = models.SmallIntegerField(default=0, verbose_name="Picking Status")
    pick_qty = models.BigIntegerField(default=0, verbose_name="Goods Pre Pick QTY")
    picked_qty = models.BigIntegerField(default=0, verbose_name="Picked QTY")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    t_code = models.CharField(max_length=255, verbose_name="Transaction Code")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'pickinglist'
        verbose_name = 'Picking List'
        verbose_name_plural = "Picking List"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid'], name='idx_pickinglist_oid'),
            models.Index(fields=['dn_code'], name='idx_pickinglist_dn'),
        ]
