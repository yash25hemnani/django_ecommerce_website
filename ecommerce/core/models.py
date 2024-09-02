from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User

STATUS_CHOICE = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
) # the first part will be used for conditonal statements

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published')
)

STATUS_CHOICE = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabets = '123456789')
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to = "category", default="This is a category") # A folder named category will be created automatically and files will be uploaded there.

    class Meta:
        verbose_name_plural = "Categories" # For pluralizing the word in the admin

    def category_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height ="50"')

    def __str__(self):
        self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabets = '123456789')
    title = models.CharField(max_length=100, default="Title Name")
    image = models.ImageField(upload_to = user_directory_path, default="vendor.jpg")
    description = models.TextField(null=True, blank=True, default="I am a product.")
    address = models.CharField(max_length=100, default="Pratap Nagar")
    contact = models.CharField(max_length=100, default="1235467895")
    chat_response_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Vendors" # For pluralizing the word in the admin

    def vendor_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height ="50"')

    def __str__(self):
        self.title


class Products(models.Models):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabets = '123456789')
    title = models.CharField(max_length=100, default="Yash")
    image = models.ImageField(upload_to = user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="Product Description")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=9999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=9999999, decimal_places=2, default="2.99")

    specifications = models.TextField(null=True, blank=True)

    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="In Review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=20, prefix='sku', alphabets = '123456789') # sku means stock keeping unit, it helps us keep track of inventory
    
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products" # For pluralizing the word in the admin

    def product_image(self):
        return mark_safe(f'<img src="{self.image.url}" width="50" height ="50"')

    def __str__(self):
        self.title

    def get_discount_percentage(self):
        new_price = (self.price/self.old_price) * 100