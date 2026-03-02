import mimetypes, os, requests, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greaterwms.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from django.conf import settings
from pathlib import Path

# PERF-006 / ISS-053: Lazy pandas import — defer heavy import until actually needed

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)

# Create required media directories
for subdir in ["win32", "linux", "darwin", "upload_example"]:
    os.makedirs(os.path.join(settings.BASE_DIR, 'media', subdir), exist_ok=True)


def _create_example_files():
    """
    Create example Excel upload templates on first run.
    PERF-006: pandas is only imported here (lazy) instead of at module level.
    """
    import pandas as pd

    templates = {
        "customer_cn.xlsx": {"index": "客户名称", "columns": {"客户名称": [], "客户城市": [], "详细地址": [], "联系电话": [], "负责人": [], "客户等级": []}},
        "customer_en.xlsx": {"index": "Customer Name", "columns": {"Customer Name": [], "Customer City": [], "Customer Address": [], "Customer Contact": [], "Customer Manager": [], "Customer Level": []}},
        "goodslist_cn.xlsx": {"index": "商品编码", "columns": {"商品编码": [], "商品描述": [], "商品供应商": [], "商品单位重量": [], "商品单位长度": [], "商品单位宽度": [], "商品单位高度": [], "最小单位体积": [], "商品单位": [], "商品类别": [], "商品品牌": [], "商品颜色": [], "商品形状": [], "商品规格": [], "商品产地": [], "商品成本": [], "商品价格": []}},
        "goodslist_en.xlsx": {"index": "Goods Code", "columns": {"Goods Code": [], "Goods Description": [], "Goods Supplier": [], "Goods Weight": [], "Goods Width": [], "Goods Depth": [], "Goods Height": [], "Unit Volume": [], "Goods Unit": [], "Goods Class": [], "Goods Brand": [], "Goods Color": [], "Goods Shape": [], "Goods Specs": [], "Goods Origin": [], "Goods Cost": [], "Goods Price": []}},
        "supplier_cn.xlsx": {"index": "供应商名称", "columns": {"供应商名称": [], "供应商城市": [], "详细地址": [], "联系电话": [], "负责人": [], "供应商等级": []}},
        "supplier_en.xlsx": {"index": "Supplier Name", "columns": {"Supplier Name": [], "Supplier City": [], "Supplier Address": [], "Supplier Contact": [], "Supplier Manager": [], "Supplier Level": []}},
    }

    for filename, spec in templates.items():
        filepath = os.path.join(settings.BASE_DIR, 'media', 'upload_example', filename)
        if not os.path.exists(filepath):
            df = pd.DataFrame(spec["columns"]).set_index(spec["index"])
            df.to_excel(filepath)


# Only create example files if they don't all exist yet
_example_dir = os.path.join(settings.BASE_DIR, 'media', 'upload_example')
if not all(os.path.exists(os.path.join(_example_dir, f)) for f in [
    'customer_cn.xlsx', 'customer_en.xlsx', 'goodslist_cn.xlsx',
    'goodslist_en.xlsx', 'supplier_cn.xlsx', 'supplier_en.xlsx'
]):
    _create_example_files()

print('Welcome To GreaterWMS')
