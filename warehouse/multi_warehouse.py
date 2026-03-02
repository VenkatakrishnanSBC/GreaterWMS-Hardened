"""
FEATURE-001: Multi-warehouse support for GreaterWMS.

Extends the existing single-warehouse model to support multiple
warehouses per tenant. Each warehouse has its own bins, stock,
and can be assigned to specific ASN/DN operations.
"""
from django.db import models


class WarehouseModel(models.Model):
    """
    Extended warehouse model for multi-warehouse support.

    Each tenant (openid) can have multiple warehouses.
    Stock, bins, ASNs, and DNs are linked to a specific warehouse.
    """
    warehouse_code = models.CharField(max_length=100, verbose_name="Warehouse Code")
    warehouse_name = models.CharField(max_length=255, verbose_name="Warehouse Name")
    warehouse_type = models.CharField(
        max_length=50, default='standard',
        choices=[
            ('standard', 'Standard Warehouse'),
            ('cold_storage', 'Cold Storage'),
            ('hazmat', 'Hazardous Materials'),
            ('cross_dock', 'Cross-Dock'),
            ('bonded', 'Bonded Warehouse'),
        ],
        verbose_name="Warehouse Type"
    )
    address = models.TextField(blank=True, default='', verbose_name="Address")
    city = models.CharField(max_length=255, blank=True, default='', verbose_name="City")
    state = models.CharField(max_length=100, blank=True, default='', verbose_name="State/Province")
    country = models.CharField(max_length=100, default='', verbose_name="Country")
    postal_code = models.CharField(max_length=20, blank=True, default='', verbose_name="Postal Code")
    latitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True,
        verbose_name="Latitude"
    )
    longitude = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True,
        verbose_name="Longitude"
    )
    contact_name = models.CharField(max_length=255, blank=True, default='', verbose_name="Contact Name")
    contact_phone = models.CharField(max_length=50, blank=True, default='', verbose_name="Contact Phone")
    contact_email = models.CharField(max_length=255, blank=True, default='', verbose_name="Contact Email")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_default = models.BooleanField(default=False, verbose_name="Default Warehouse")
    max_capacity = models.BigIntegerField(default=0, verbose_name="Max Capacity (units)")
    current_utilization = models.BigIntegerField(default=0, verbose_name="Current Utilization")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'warehouse_extended'
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['warehouse_name']
        unique_together = [['warehouse_code', 'openid']]
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_wh_ext_oid_del'),
            models.Index(fields=['warehouse_code'], name='idx_wh_ext_code'),
            models.Index(fields=['openid', 'is_active'], name='idx_wh_ext_oid_active'),
        ]

    def __str__(self) -> str:
        return f"{self.warehouse_code} - {self.warehouse_name}"


class WarehouseZoneModel(models.Model):
    """
    Zones within a warehouse (e.g., receiving, shipping, storage).

    Zones help organize bins and define operational areas.
    """
    warehouse = models.ForeignKey(
        WarehouseModel, on_delete=models.CASCADE,
        related_name='zones', verbose_name="Warehouse"
    )
    zone_code = models.CharField(max_length=50, verbose_name="Zone Code")
    zone_name = models.CharField(max_length=255, verbose_name="Zone Name")
    zone_type = models.CharField(
        max_length=50, default='storage',
        choices=[
            ('receiving', 'Receiving'),
            ('storage', 'Storage'),
            ('picking', 'Picking'),
            ('packing', 'Packing'),
            ('shipping', 'Shipping'),
            ('staging', 'Staging'),
            ('returns', 'Returns'),
            ('quarantine', 'Quarantine'),
        ],
        verbose_name="Zone Type"
    )
    temperature_controlled = models.BooleanField(default=False, verbose_name="Temperature Controlled")
    min_temp_celsius = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name="Min Temperature (°C)"
    )
    max_temp_celsius = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        verbose_name="Max Temperature (°C)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Update Time")

    class Meta:
        db_table = 'warehouse_zone'
        verbose_name = 'Warehouse Zone'
        verbose_name_plural = 'Warehouse Zones'
        ordering = ['zone_code']
        unique_together = [['warehouse', 'zone_code']]

    def __str__(self) -> str:
        return f"{self.warehouse.warehouse_code}/{self.zone_code}"


class InterWarehouseTransfer(models.Model):
    """
    Track transfers between warehouses.

    When stock is moved from one warehouse to another,
    a transfer record captures the transaction.
    """
    transfer_code = models.CharField(max_length=255, unique=True, verbose_name="Transfer Code")
    from_warehouse = models.ForeignKey(
        WarehouseModel, on_delete=models.CASCADE,
        related_name='outbound_transfers', verbose_name="From Warehouse"
    )
    to_warehouse = models.ForeignKey(
        WarehouseModel, on_delete=models.CASCADE,
        related_name='inbound_transfers', verbose_name="To Warehouse"
    )
    status = models.CharField(
        max_length=20, default='pending',
        choices=[
            ('pending', 'Pending'),
            ('in_transit', 'In Transit'),
            ('received', 'Received'),
            ('cancelled', 'Cancelled'),
        ],
        verbose_name="Transfer Status"
    )
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    transfer_qty = models.BigIntegerField(default=0, verbose_name="Transfer Quantity")
    received_qty = models.BigIntegerField(default=0, verbose_name="Received Quantity")
    notes = models.TextField(blank=True, default='', verbose_name="Notes")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, verbose_name="Update Time")

    class Meta:
        db_table = 'inter_warehouse_transfer'
        verbose_name = 'Inter-Warehouse Transfer'
        verbose_name_plural = 'Inter-Warehouse Transfers'
        ordering = ['-create_time']
        indexes = [
            models.Index(fields=['openid', 'status'], name='idx_iwt_oid_status'),
            models.Index(fields=['transfer_code'], name='idx_iwt_code'),
        ]

    def __str__(self) -> str:
        return f"{self.transfer_code}: {self.from_warehouse} → {self.to_warehouse}"
