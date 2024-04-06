import csv
import decimal
from decimal import Decimal
from products_shop.models import Product
from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from category.models import Category

class Command(BaseCommand):
    help = 'Load data from csv'

    def handle(self, *args, **options):

        # drop the data from the table so that if we rerun the file, we don't repeat values
        Category.objects.all().delete()
        Product.objects.all().delete()
        print("tables dropped successfully")
        # create table again

        # Create categories and assign products
        file_path = 'products_shop/dataset/mobileshop.csv'
        parsed_data = parse_csv_file(file_path)
        create_categories_from_csv(parsed_data)
        assign_products_to_categories(parsed_data)


def parse_csv_file(file_path):
    parsed_data = []
    with open(file_path, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        next(reader) # skip the header line
        for row in reader:
            # Extracting required columns from each row
            product_description = {
                'battery_capacity': row.get('Battery capacity (mAh)'),
                'processor': row.get('Processor'),
                'operating_system': row.get('Operating system'),
                'rear_camera': row.get('Rear camera'),
                'front_camera': row.get('Front camera'),
                'internal_storage': row.get('Internal storage'),
                'resolution': row.get('Resolution'),
                'ram': row.get('RAM'),
                'form_factor': row.get('Form factor'),
                'screen_size': row.get('Screen size (inches)'),
                'wifi': row.get('Wi-Fi'),
                'bluetooth': row.get('Bluetooth'),
                'touchscreen': row.get('Touchscreen'),
                'expandable_storage': row.get('Expandable storage'),
                'launched': row.get('Launched'),
                'accelerometer': row.get('Accelerometer'),
                'gps': row.get('GPS'),
                'number_of_sims': row.get('Number of SIMs'),
                'sim_1_4g_lte': row.get('Sim 1 4G/ LTE'),
                'sim_2_4g_lte': row.get('Sim 2 4G/ LTE'),
                'sim_1_3g': row.get('Sim 1 3G'),
                'sim_2_3g': row.get('Sim 2 3G'),
                'sim_2_gsm_cdma': row.get('Sim 2 GSM/CDMA'),
                'sim_1_gsm_cdma': row.get('Sim 1 GSM/CDMA'),
                'proximity_sensor': row.get('Proximity sensor'),
                'ambient_light_sensor': row.get('Ambient light sensor'),
                'rear_flash': row.get('Rear flash'),
                'compass_magnetometer': row.get('Compass/ Magnetometer'),
                'gyroscope': row.get('Gyroscope'),
                'expandable_storage_type': row.get('Expandable storage type'),
                'headphones': row.get('Headphones'),
                'removable_battery': row.get('Removable battery'),
                'dimensions': row.get('Dimensions (mm)'),
                'colours': row.get('Colours'),
                'expandable_storage_up_to_gb': row.get('Expandable storage up to (GB)'),
                'fm': row.get('FM'),
                'nfc': row.get('NFC'),
                'usb_otg': row.get('USB OTG'),
                'wifi_direct': row.get('Wi-Fi Direct'),
                'processor_make': row.get('Processor make'),
                'infrared': row.get('Infrared'),
                'other_info': row.get('other_info'),
            }
            # Adding product description to parsed data
            parsed_row = {
                'product_description': product_description,
                'url': row.get('url'),
                'brand': row.get('Brand'),
                'product_name': row.get('Product Name'),
                'model': row.get('Model'),
                'picture_url': row.get('Picture URL'),
                'price_in_gbp': row.get('Price in GBP'),
            }
            parsed_data.append(parsed_row)
    return parsed_data

# Usage:
file_path = 'products_shop/dataset/mobileshop.csv'
parsed_data = parse_csv_file(file_path)
# print(parsed_data)  # Use or store the parsed data as needed


def create_categories_from_csv(parsed_data):
    # Extract unique values from the 'Operating system' column
    operating_systems = set(item['product_description']['operating_system'] for item in parsed_data)
    
    # Create a category for each unique operating system
    for os in operating_systems:
        category_name = os.strip()  # Remove leading/trailing whitespace
        # Check if the category already exists
        category, created = Category.objects.get_or_create(cat_name=category_name)
        if created:
            print(f"Created category: {category_name}")

# Usage example
parsed_data = parse_csv_file('products_shop/dataset/mobileshop.csv')
create_categories_from_csv(parsed_data)


def preprocess_price(price_str):
    # Convert the price string to a decimal number
    try:
        return Decimal(price_str.strip('£'))  # Assuming prices are in GBP
    except Exception as e:
        # Handle any errors during price preprocessing
        print(f"Error preprocessing price: {e}")
        return None  # Return None if preprocessing fails


def assign_products_to_categories(parsed_data):
    # Assign each product to its corresponding category based on the 'Operating system' column
    for item in parsed_data:
        try:
            os = item['product_description']['operating_system'].strip()  # Remove leading/trailing whitespace
            product_name = item['product_name']
            price_str = item['price_in_gbp']
            price = preprocess_price(price_str)
            image_url = item['picture_url']
            product_description = item['product_description']
            # Get or create the category for the operating system
            category, _ = Category.objects.get_or_create(cat_name=os)
            # Check if a product with the same category name already exists
            if not Product.objects.filter(product_name=product_name, category=category).exists():            
            # Create the product only if price is successfully processed
                if price is not None:
                    # Check if a product with the same category name already exists
                    if not Product.objects.filter(product_name=product_name, category=category).exists():
                        Product.objects.create(
                            product_name=product_name,
                            price=price,
                            product_description=product_description,
                            image_url=image_url,
                            category=category
                        )
            else:
                print(f"Product '{product_name}' with category '{category.cat_name}' already exists.")
        except Exception as e:
            print(f"Error creating product: {e}")

# Usage example
parsed_data = parse_csv_file('products_shop/dataset/mobileshop.csv')
assign_products_to_categories(parsed_data)
