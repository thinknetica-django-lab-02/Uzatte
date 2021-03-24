from main.models import Category, Good

# Creating objects via constructor + save() method

iphone_12_pro = Good(name="iPhone 12 Pro",
                     description="Apple iPhone",
                     price="98000.00")
iphone_12_pro.save()
samsung_galaxy_s20 = Good(name="Samsung Galaxy S20",
                          description="Samsung",
                          price="95000.00")
samsung_galaxy_s20.save()
phone_category = Category(name="Phones",
                          description="Phones and Smartphones")
phone_category.save()

# Creating objects via objects.create() method

macbook_air_2020 = Good.objects.create(name="Macbook Air 2020",
                                       description="Apple Laptop",
                                       price="120000")
acer_nitro_5 = Good.objects.create(name="Acer Nitro 5",
                                   description="Acer Laptop",
                                   price="105000")
laptop_category = Category.objects.create(name="Laptops",
                                          description="Laptops and Notebooks")

# Adding category to goods

iphone_12_pro.categories.add(phone_category)
samsung_galaxy_s20.categories.add(phone_category)
macbook_air_2020.categories.add(laptop_category)
acer_nitro_5.categories.add(laptop_category)

# Getting different categories via objects.filter() method

Good.objects.filter(categories__name="Laptops")
# output:<QuerySet [<Good: Macbook Air 2020>, <Good: Acer Nitro 5>]>
Good.objects.filter(categories__name="Phones")
# output:<QuerySet [<Good: iPhone 12 Pro>, <Good: Samsung Galaxy S20>]>
Good.objects.filter(name="Macbook Air 2020")
# output:<QuerySet [<Good: Macbook Air 2020>]>
Good.objects.filter(price__gte=100000)
# output: <QuerySet [<Good: Macbook Air 2020>, <Good: Acer Nitro 5>]>
Good.objects.filter(name__startswith="A")
# output: <QuerySet [<Good: Acer Nitro 5>]>
