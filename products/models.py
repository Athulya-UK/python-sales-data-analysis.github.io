from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=220)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)
class Purchase(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField(blank=True)
    salesman=models.CharField(max_length=210)
    salesman_emailid=models.CharField(max_length=100,default="")
    branchname=models.CharField(max_length=100)
    date=models.DateTimeField(default=timezone.now)
    def save(self,*args,**kwargs):
        self.total_price=self.price*self.quantity
        super().save(*args,**kwargs)
    
    def __str__(self):
        return "solled {} - {} items for {}".format(self.product.name,self.quantity,self.total_price)