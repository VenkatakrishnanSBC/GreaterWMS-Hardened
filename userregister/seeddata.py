"""
ARCH-006: Demo data seeding extracted from registration view.

This module contains all the demo/sample data creation logic that was formerly
inlined in the register() function. This separation:
  1. Makes register() focused on authentication (SRP)
  2. Makes demo data independently testable
  3. Reduces register() from 435 lines to ~60 lines
"""
import random
import os
from typing import List
from django.conf import settings
from utils.md5 import Md5

# --- Random data pools (moved from module-level in views.py) ---

CITIES: List[str] = [
    "shanghai", "nanjing", "hangzhou", "beijing", "chongqing",
    "shenzhen", "guangzhou", "suzhou", "hefei", "chengdu", "kunming", "wuhan"
]

COLORS: List[str] = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Purple"]

SHAPES: List[str] = ["Square", "Rectangle", "Cone", "Cylinder", "Irregular"]

SPECS: List[str] = ["1 x 10", "3 x 3", "5 x 5", "6 x 6"]

UNITS: List[str] = ["Pcs", "Box", "Pair"]

CLASSES: List[str] = ["Electronics", "Grocery", "Medical", "Industrial"]

NAMES: List[str] = [
    "Abigail", "Alexandra", "Alison", "Amanda", "Amelia", "Amy",
    "Andrew", "Angela", "Anna", "Anne", "Anthony", "Austin",
    "Benjamin", "Blake", "Boris", "Brandon", "Brian",
    "Cameron", "Caroline", "Charles", "Christian", "Christopher",
    "Colin", "Connor", "Dan", "David", "Dominic", "Dylan",
    "Edward", "Elizabeth", "Emily", "Emma", "Eric", "Evan",
    "Faith", "Felicity", "Fiona", "Frank", "Gavin", "Grace",
    "Hannah", "Harry", "Heather", "Ian", "Irene", "Isaac",
    "Jack", "Jacob", "Jake", "James", "Jan", "Jane", "Jason",
    "Jennifer", "Jessica", "Joan", "Joe", "John", "Jonathan",
    "Joseph", "Joshua", "Julia", "Justin", "Karen", "Katherine",
    "Keith", "Kevin", "Kimberly", "Kylie", "Lauren", "Leah",
    "Leonard", "Liam", "Lillian", "Lily", "Lucas", "Luke",
    "Madeleine", "Maria", "Mary", "Matt", "Max", "Megan",
    "Melanie", "Michael", "Michelle", "Molly", "Natalie", "Nathan",
    "Neil", "Nicholas", "Nicole", "Oliver", "Olivia", "Owen",
    "Penelope", "Peter", "Phil", "Piers", "Pippa", "Rachel",
    "Rebecca", "Richard", "Robert", "Rose", "Ruth", "Ryan",
    "Sally", "Samantha", "Samuel", "Sarah", "Sebastian", "Simon",
    "Sonia", "Sophie", "Stephanie", "Stephen", "Stewart", "Sue",
    "Theresa", "Thomas", "Tim", "Tracey", "Trevor", "Una",
    "Vanessa", "Victor", "Victoria", "Virginia", "Wanda", "Warren",
    "Wendy", "William", "Xanthe", "Yasmine",
    "Yale", "Yedda", "Yehudi", "Zachary", "Zebulon", "Zenobia"
]

BIN_SIZES: List[str] = ["Big", "Floor", "Tiny", "Small"]
BIN_PROPERTIES: List[str] = ["Normal", "Holding", "Damage", "Inspection"]
STAFF_TYPES: List[str] = ["Admin", "Inbound", "Outbound", "QC"]


def random_phone() -> str:
    """Generate a random phone number."""
    return "".join(random.choice("0123456789") for _ in range(11))


def random_staff_type() -> str:
    """Pick a random staff type."""
    return random.choice(STAFF_TYPES)


def seed_demo_data(openid: str) -> None:
    """
    Create all demo/sample data for a newly registered user.

    Args:
        openid: The tenant identifier for the new user.
    """
    # --- Media directories ---
    media_base = os.path.join(settings.BASE_DIR, 'media', openid)
    for subdir in ["", "win32", "linux", "darwin"]:
        os.makedirs(os.path.join(media_base, subdir), exist_ok=True)

    # --- Company & Warehouse ---
    from company.models import ListModel as company
    company.objects.create(
        openid=openid, company_name='GreaterWMS',
        company_city=random.choice(CITIES),
        company_address="People's Square # 666 Room 1F",
        company_contact=random_phone(),
        company_manager='Elvis.Shi', creater='DemoData'
    )
    from warehouse.models import ListModel as warehouse
    warehouse.objects.create(
        openid=openid, warehouse_name='Center Warehouse',
        warehouse_city=random.choice(CITIES),
        warehouse_address="People's Square # 666 Room 2F",
        warehouse_contact=random_phone(),
        warehouse_manager='Tim.Yao', creater='DemoData'
    )

    # --- Suppliers (41) ---
    from supplier.models import ListModel as supplier
    supplier.objects.bulk_create([
        supplier(
            openid=openid, supplier_name=f'Supplier Name-{i}',
            supplier_city=random.choice(CITIES),
            supplier_address=f'Address-{i}',
            supplier_contact=random_phone(),
            supplier_manager=random.choice(NAMES), creater='DemoData'
        ) for i in range(1, 42)
    ], batch_size=100)

    # --- Customers (41) ---
    from customer.models import ListModel as customer
    customer.objects.bulk_create([
        customer(
            openid=openid, customer_name=f'Customer Name-{i}',
            customer_city=random.choice(CITIES),
            customer_address=f'Address-{i}',
            customer_contact=random_phone(),
            customer_manager=random.choice(NAMES), creater='DemoData'
        ) for i in range(1, 42)
    ], batch_size=100)

    # --- Staff ---
    from staff.models import ListModel as staff_model
    staff_model.objects.bulk_create([
        staff_model(
            openid=openid, staff_name=name,
            staff_type=random_staff_type(),
            check_code=random.randint(1000, 9999)
        ) for name in NAMES
    ], batch_size=100)

    # --- Drivers (41) ---
    from driver.models import ListModel as driver
    driver.objects.bulk_create([
        driver(
            openid=openid, driver_name=f'Driver Name-{i}',
            license_plate="".join(random.choice("0123456789") for _ in range(8)),
            contact=random_phone(), creater='DemoData'
        ) for i in range(1, 42)
    ], batch_size=100)

    # --- Capital (41) ---
    from capital.models import ListModel as capital
    capital.objects.bulk_create([
        capital(
            openid=openid, capital_name=f'Capital Name-{i}',
            capital_qty=random.randint(1, 100),
            capital_cost=random.randint(100, 10000), creater='DemoData'
        ) for i in range(1, 42)
    ], batch_size=100)

    # --- Bin Sizes ---
    from binsize.models import ListModel as binsize
    binsize.objects.bulk_create([
        binsize(openid=openid, bin_size='Big', bin_size_w=1100, bin_size_d=1200, bin_size_h=1800, creater='DemoData'),
        binsize(openid=openid, bin_size='Floor', bin_size_w=10000, bin_size_d=10000, bin_size_h=10000, creater='DemoData'),
        binsize(openid=openid, bin_size='Small', bin_size_w=800, bin_size_d=1000, bin_size_h=1200, creater='DemoData'),
        binsize(openid=openid, bin_size='Tiny', bin_size_w=200, bin_size_d=250, bin_size_h=300, creater='DemoData'),
    ], batch_size=100)

    # --- Bin Set (12 bins) + Scanner entries ---
    from binset.models import ListModel as binset
    from scanner.models import ListModel as scanner
    bin_configs = [
        ('A010101', 'Normal'), ('A010102', 'Normal'), ('A010103', 'Normal'),
        ('B010101', 'Inspection'), ('B010102', 'Inspection'), ('B010103', 'Inspection'),
        ('B020101', 'Holding'), ('B020102', 'Holding'), ('B020103', 'Holding'),
        ('B030101', 'Damage'), ('B030102', 'Damage'), ('B030103', 'Damage'),
    ]
    binset_list = []
    for idx, (name, prop) in enumerate(bin_configs, 1):
        bar_code = Md5.md5(str(idx))
        binset_list.append(binset(
            openid=openid, bin_name=name,
            bin_size=random.choice(BIN_SIZES),
            bin_property=prop, empty_label=True,
            creater='DemoData', bar_code=bar_code
        ))
        scanner.objects.create(
            openid=openid, mode="BINSET",
            code=name, bar_code=bar_code
        )
    binset.objects.bulk_create(binset_list, batch_size=100)

    # --- Goods metadata (units, classes, colors, brands, shapes, specs, origins) ---
    from goodsunit.models import ListModel as goodsunit
    goodsunit.objects.bulk_create([
        goodsunit(openid=openid, goods_unit=u, creater='DemoData') for u in UNITS
    ], batch_size=100)

    from goodsclass.models import ListModel as goodsclass
    goodsclass.objects.bulk_create([
        goodsclass(openid=openid, goods_class=c, creater='DemoData') for c in CLASSES
    ], batch_size=100)

    from goodscolor.models import ListModel as goodscolor
    goodscolor.objects.bulk_create([
        goodscolor(openid=openid, goods_color=c, creater='DemoData') for c in COLORS
    ], batch_size=100)

    from goodsbrand.models import ListModel as goodsbrand
    goodsbrand.objects.bulk_create([
        goodsbrand(openid=openid, goods_brand=f'Brand Name-{i}', creater='DemoData')
        for i in range(1, 42)
    ], batch_size=100)

    from goodsshape.models import ListModel as goodsshape
    goodsshape.objects.bulk_create([
        goodsshape(openid=openid, goods_shape=s, creater='DemoData') for s in SHAPES
    ], batch_size=100)

    from goodsspecs.models import ListModel as goodsspecs
    goodsspecs.objects.bulk_create([
        goodsspecs(openid=openid, goods_specs=s, creater='DemoData') for s in SPECS
    ], batch_size=100)

    from goodsorigin.models import ListModel as goodsorigin
    goodsorigin.objects.bulk_create([
        goodsorigin(openid=openid, goods_origin=c, creater='DemoData') for c in CITIES
    ], batch_size=100)

    # --- Goods (41 items) ---
    from goods.models import ListModel as goods
    goods_list = []
    for i in range(1, 42):
        bar_code = Md5.md5(f"A0000{i}")
        goods_w = round(random.uniform(10, 1000), 2)
        goods_d = round(random.uniform(10, 1000), 2)
        goods_h = round(random.uniform(10, 1000), 2)
        goods_cost = round(random.uniform(10, 1000), 2)
        goods_price = round(random.uniform(goods_cost + 1, 2000), 2)
        goods_list.append(goods(
            openid=openid, goods_code=f"A0000{i}",
            goods_desc=f"Goods Desc-{i}",
            goods_supplier=f'Supplier Name-{random.randint(1, 41)}',
            goods_weight=random.randint(100, 10000),
            goods_w=goods_w, goods_d=goods_d, goods_h=goods_h,
            unit_volume=round((goods_w * goods_d * goods_h) / 1e9, 4),
            goods_unit=random.choice(UNITS), goods_class=random.choice(CLASSES),
            goods_brand=f'Brand Name-{random.randint(1, 41)}',
            goods_color=random.choice(COLORS), goods_shape=random.choice(SHAPES),
            goods_specs=random.choice(SPECS), goods_origin=random.choice(CITIES),
            goods_cost=goods_cost, goods_price=goods_price,
            bar_code=bar_code, creater='DemoData'
        ))
        scanner.objects.create(
            openid=openid, mode="GOODS",
            code=f"A0000{i}", bar_code=bar_code
        )
    goods.objects.bulk_create(goods_list, batch_size=100)

    # --- Transportation fees (city × city matrix) ---
    from payment.models import TransportationFeeListModel as freight
    freight.objects.bulk_create([
        freight(
            openid=openid, send_city=sender, receiver_city=receiver,
            weight_fee=random.randint(10, 20),
            volume_fee=random.randint(100, 200),
            min_payment=random.randint(250, 300),
            transportation_supplier="Supplier", creater="DemoData"
        )
        for sender in CITIES for receiver in CITIES
    ], batch_size=100)
