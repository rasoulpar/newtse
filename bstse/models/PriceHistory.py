from django.db import models

class PriceHistory(models.Model):
    columns=['Date', 'High', 'Low', 'Close', 'Last', 'First', 'Open', 'TradesValue', 'Volume', 'TradesCount']
    Date = models.CharField(max_length=8)
    High = models.FloatField()
    Low = models.FloatField()
    Close = models.FloatField()
    Last = models.FloatField()
    Open = models.FloatField()
    TradesValue = models.FloatField()
    Volume = models.FloatField()
    TradesCount = models.IntegerField()