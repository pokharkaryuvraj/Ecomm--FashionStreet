from django.db import models
from django.contrib.auth.models import User
from django.db import migrations

# Create your models here.
class Wear(models.Model):

    name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)
    price = models.FloatField()
    pimage = models.ImageField(upload_to='image')

class Cart(models.Model):

    sid = models.ForeignKey(Wear, on_delete=models.CASCADE,db_column='sid')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    order_id = models.IntegerField()
    sid = models.ForeignKey(Wear, on_delete=models.CASCADE,db_column='sid') 
    uid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    quantity = models.IntegerField(default=1)


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp','0006_remove_order_sid_order_wid'),
    ]

    operations = [
        migrations.AddField(
            model_name='Wear',
            name='sid',
            field=models.CharField(max_length=100, blank=True), # Change the field type and length as per your requirement
        ),
    ]

   