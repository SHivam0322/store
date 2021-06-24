from django.db import models

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    desc=models.CharField(max_length=2000)
    pub_date = models.DateField()
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price =models.IntegerField(default=0)
    image = models.ImageField(upload_to="store/images", default="")

    def __str__(self):
       return self.product_name

class Contact(models.Model):
    msg_id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    number=models.IntegerField(default="")
    issue=models.CharField(max_length=500)

    def __str__(self):
        return self.name