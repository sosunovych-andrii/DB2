import mysql.connector
from src.database.settings_mongodb import get_mongo
from decimal import Decimal

def migrate_all_to_mongodb(clear_before_insert: bool = False):
    print("Початок повної нормалізованої міграції...")

    mysql_conn = mysql.connector.connect(
        host="db", port=3306,
        user="root", password="password",
        database="my_database"
    )
    cursor = mysql_conn.cursor(dictionary=True)

    mongo_db = get_mongo()
    manufacturers_col = mongo_db["manufacturers"]
    product_types_col = mongo_db["product_types"]
    price_lists_col = mongo_db["price_lists"]
    sales_col = mongo_db["sales"]

    if clear_before_insert:
        manufacturers_col.delete_many({})
        product_types_col.delete_many({})
        price_lists_col.delete_many({})
        sales_col.delete_many({})
        print("Всі колекції очищені")

    cursor.execute("SELECT id, name FROM manufacturers")
    manufacturers = cursor.fetchall()
    if manufacturers:
        manufacturers_col.insert_many(manufacturers)
        print(f"Вставлено {len(manufacturers)} виробників")

    cursor.execute("SELECT id, name FROM product_types")
    product_types = cursor.fetchall()
    if product_types:
        product_types_col.insert_many(product_types)
        print(f"Вставлено {len(product_types)} типів продукції")

    cursor.execute("""
        SELECT id, unit_price, manufacturer_id, product_type_id 
        FROM price_list
    """)
    price_lists = cursor.fetchall()
    for item in price_lists:
        if isinstance(item.get("unit_price"), Decimal):
            item["unit_price"] = float(item["unit_price"])
    if price_lists:
        price_lists_col.insert_many(price_lists)
        print(f"Вставлено {len(price_lists)} записів прайс-листа")

    cursor.execute("""
        SELECT id, amount, sale_date, payment_date, price_list_id 
        FROM sales
    """)
    sales = cursor.fetchall()

    for sale in sales:
        if sale.get("sale_date"):
            sale["sale_date"] = sale["sale_date"].isoformat()
        if sale.get("payment_date"):
            sale["payment_date"] = sale["payment_date"].isoformat()

    if sales:
        sales_col.insert_many(sales)
        print(f"Вставлено {len(sales)} продажів")

    cursor.close()
    mysql_conn.close()

    print("Міграція успішно завершена!")


if __name__ == "__main__":
    migrate_all_to_mongodb(clear_before_insert=True)
