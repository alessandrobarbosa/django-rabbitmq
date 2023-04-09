from django.db import models


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=200)


class ProductUser(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'product'],
                name='user_product_unique'
            )
        ]
