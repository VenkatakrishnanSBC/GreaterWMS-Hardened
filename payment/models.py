from django.db import models

class TransportationFeeListModel(models.Model):
    send_city = models.CharField(max_length=255, verbose_name="Send City")
    receiver_city = models.CharField(max_length=255, verbose_name="Receiver City")
    weight_fee = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Weight Fee")    # DB-003
    volume_fee = models.DecimalField(max_digits=12, decimal_places=4, default=0, verbose_name="Volume Fee")    # DB-003
    min_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Min Payment")  # DB-003
    transportation_supplier = models.CharField(max_length=255, verbose_name="Transportation Supplier")
    creater = models.CharField(max_length=255, verbose_name="Who Created")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'transportationfee'
        verbose_name = 'Transportation Fee'
        verbose_name_plural = "Transportation Fee"
        ordering = ['-id']
        # DB-002 / ISS-010: Database indexes
        indexes = [
            models.Index(fields=['openid', 'is_delete'], name='idx_transfee_oid_del'),
        ]
