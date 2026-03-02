from django.db import models


class AsnListModel(models.Model):
    asn_code = models.CharField(max_length=255, verbose_name="ASN Code")
    asn_status = models.BigIntegerField(default=1, verbose_name="ASN Status")
    total_weight = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Total Weight")   # DB-003 / ISS-011
    total_volume = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Total Volume")   # DB-003 / ISS-011
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Cost")       # DB-003 / ISS-011
    supplier = models.CharField(max_length=255, verbose_name="ASN Supplier")
    # DB-005: ForeignKey to Supplier model (nullable for backward compatibility)
    supplier_fk = models.ForeignKey(
        'supplier.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='asn_orders',
        verbose_name="Supplier Reference", db_column='supplier_fk_id'
    )
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    bar_code = models.CharField(max_length=255, verbose_name="Bar Code")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    transportation_fee = models.JSONField(default=dict, verbose_name="Transportation Fee")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'asnlist'
        verbose_name = 'ASN List'
        verbose_name_plural = "ASN List"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_asnlist_oid_del'),
            models.Index(fields=['asn_code'], name='idx_asnlist_asn_code'),
            models.Index(fields=['openid', 'asn_status'], name='idx_asnlist_oid_status'),
        ]


class AsnDetailModel(models.Model):
    asn_code = models.CharField(max_length=255, verbose_name="ASN Code")
    # DB-005: ForeignKey to parent ASN list
    asn_list = models.ForeignKey(
        AsnListModel, on_delete=models.CASCADE,
        null=True, blank=True, related_name='details',
        verbose_name="ASN List Reference"
    )
    asn_status = models.BigIntegerField(default=1, verbose_name="ASN Status")
    supplier = models.CharField(max_length=255, verbose_name="ASN Supplier")
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    # DB-005: ForeignKey to Goods model
    goods_fk = models.ForeignKey(
        'goods.ListModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='asn_details',
        verbose_name="Goods Reference"
    )
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    goods_qty = models.BigIntegerField(default=0, verbose_name="Goods QTY")
    goods_actual_qty = models.BigIntegerField(default=0, verbose_name="Goods Actual QTY")
    sorted_qty = models.BigIntegerField(default=0, verbose_name="Sorted QTY")
    goods_shortage_qty = models.BigIntegerField(default=0, verbose_name="Goods Shortage QTY")
    goods_more_qty = models.BigIntegerField(default=0, verbose_name="Goods More QTY")
    goods_damage_qty = models.BigIntegerField(default=0, verbose_name="Goods damage QTY")
    goods_weight = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Goods Weight")   # DB-003 / ISS-011
    goods_volume = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Goods Volume")   # DB-003 / ISS-011
    goods_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Goods Cost")       # DB-003 / ISS-011
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'asndetail'
        verbose_name = 'ASN Detail'
        verbose_name_plural = "ASN Detail"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_asndetail_oid_del'),
            models.Index(fields=['asn_code'], name='idx_asndetail_asn_code'),
            models.Index(fields=['goods_code'], name='idx_asndetail_gc'),
        ]

