from django.db import models
from shortuuidfield import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User

# choices will print out a checkbox with the given fields
# the first part will be used for conditonal statements
# The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name

STATUS_CHOICE = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered')
) 

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published')
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, max_length=20)
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
    vid = ShortUUIDField(unique=True, max_length=20)
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


class Product(models.Model):
    pid = ShortUUIDField(unique=True, max_length=20)
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

    sku = ShortUUIDField(unique=True, max_length=20) # sku means stock keeping unit, it helps us keep track of inventory
    
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


class Product_Images(models.Model):
    images = models.ImageField(upload_to='product_images', default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

############################################################################################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Orders"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=9999999, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe(f'<img src="/media/{self.image}" width="50" height ="50">')

############################################################################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews" # For pluralizing the word in the admin

    def __str__(self):
        return self.product.title
     
    def get_rating(self):
        return self.rating
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist" # For pluralizing the word in the admin

    def __str__(self):
        return self.product.title
     
    def get_rating(self):
        return self.rating
    
 
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses" 