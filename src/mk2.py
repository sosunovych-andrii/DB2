from src.database.settings_mongodb import get_mongo


db = get_mongo()


distributors = [
  {
    "code": 1000,
    "name": "August Gumplmayr",
    "address": "4010, Feldkirchen A.D. Donau Badmuhllacken, 26",
    "country": "Німеччина"
  },
  {
    "code": 2000,
    "name": "Alfa Ltd",
    "address": "75 King Street Po Box 738, Hammersmith, London",
    "country": "Великобританія"
  },
  {
    "code": 3000,
    "name": "Cerdec ag",
    "address": "Salyufer 6-8, D-10587, Berlin",
    "country": "Німеччина"
  }
]


orders = [
  {
    "order_id": 1,
    "distributor_code": 1000,
    "order_date": "2004-03-21",
    "payment_date": "2004-03-25",
    "contents": [
      {
        "good_code": 211,
        "good_name": "Водонагрівачі Fismar 30л",
        "price": 45,
        "quantity": 1
      },
      {
        "good_code": 311,
        "good_name": "Водонагрівачі Gorenje 50л",
        "price": 140,
        "quantity": 5
      }
    ]
  },
  {
    "order_id": 2,
    "distributor_code": 2000,
    "order_date": "2004-03-24",
    "payment_date": "2004-04-06",
    "contents": [
      {
        "good_code": 411,
        "good_name": "Колонки газові Gorenje 13л/ хв.",
        "price": 120,
        "quantity": 10
      },
      {
        "good_code": 511,
        "good_name": "Колонки газові Bayard 16л/ хв.",
        "price": 160,
        "quantity": 15
      }
    ]
  },
  {
    "order_id": 3,
    "distributor_code": 3000,
    "order_date": "2004-03-27",
    "payment_date": "2004-03-31",
    "contents": [
      {
        "good_code": 611,
        "good_name": "Кухонний комбайн Kenwood",
        "price": 180,
        "quantity": 18
      },
      {
        "good_code": 211,
        "good_name": "Водонагрівачі Fismar 30л",
        "price": 45,
        "quantity": 12
      }
    ]
  },
  {
    "order_id": 4,
    "distributor_code": 1000,
    "order_date": "2004-03-30",
    "payment_date": "2004-04-05",
    "contents": [
      {
        "good_code": 311,
        "good_name": "Водонагрівачі Gorenje 50л",
        "price": 140,
        "quantity": 9
      },
      {
        "good_code": 411,
        "good_name": "Колонки газові Gorenje 13л/ хв.",
        "price": 120,
        "quantity": 5
      }
    ]
  },
  {
    "order_id": 5,
    "distributor_code": 2000,
    "order_date": "2004-04-02",
    "payment_date": "2004-04-06",
    "contents": [
      {
        "good_code": 511,
        "good_name": "Колонки газові Bayard 16л/ хв.",
        "price": 160,
        "quantity": 10
      },
      {
        "good_code": 611,
        "good_name": "Кухонний комбайн Kenwood",
        "price": 180,
        "quantity": 1
      }
    ]
  },
  {
    "order_id": 6,
    "distributor_code": 3000,
    "order_date": "2004-04-05",
    "payment_date": "2004-04-09",
    "contents": [
      {
        "good_code": 211,
        "good_name": "Водонагрівачі Fismar 30л",
        "price": 45,
        "quantity": 5
      },
      {
        "good_code": 311,
        "good_name": "Водонагрівачі Gorenje 50л",
        "price": 140,
        "quantity": 6
      }
    ]
  },
  {
    "order_id": 7,
    "distributor_code": 1000,
    "order_date": "2004-04-04",
    "payment_date": None,
    "contents": [
      {
        "good_code": 411,
        "good_name": "Колонки газові Gorenje 13л/ хв.",
        "price": 120,
        "quantity": 2
      },
      {
        "good_code": 511,
        "good_name": "Колонки газові Bayard 16л/ хв.",
        "price": 160,
        "quantity": 14
      }
    ]
  },
  {
    "order_id": 8,
    "distributor_code": 2000,
    "order_date": "2004-04-11",
    "payment_date": "2004-04-12",
    "contents": [
      {
        "good_code": 611,
        "good_name": "Кухонний комбайн Kenwood",
        "price": 180,
        "quantity": 15
      },
      {
        "good_code": 211,
        "good_name": "Водонагрівачі Fismar 30л",
        "price": 45,
        "quantity": 11
      }
    ]
  },
  {
    "order_id": 9,
    "distributor_code": 3000,
    "order_date": "2004-04-14",
    "payment_date": "2004-04-15",
    "contents": [
      {
        "good_code": 311,
        "good_name": "Водонагрівачі Gorenje 50л",
        "price": 140,
        "quantity": 12
      },
      {
        "good_code": 411,
        "good_name": "Колонки газові Gorenje 13л/ хв.",
        "price": 120,
        "quantity": 9
      }
    ]
  },
  {
    "order_id": 10,
    "distributor_code": 1000,
    "order_date": "2004-04-17",
    "payment_date": "2004-04-18",
    "contents": [
      {
        "good_code": 511,
        "good_name": "Колонки газові Bayard 16л/ хв.",
        "price": 160,
        "quantity": 8
      },
      {
        "good_code": 611,
        "good_name": "Кухонний комбайн Kenwood",
        "price": 180,
        "quantity": 3
      }
    ]
  },
  {
    "order_id": 11,
    "distributor_code": 2000,
    "order_date": "2004-04-20",
    "payment_date": None,
    "contents": [
      {
        "good_code": 211,
        "good_name": "Водонагрівачі Fismar 30л",
        "price": 45,
        "quantity": 5
      },
      {
        "good_code": 311,
        "good_name": "Водонагрівачі Gorenje 50л",
        "price": 140,
        "quantity": 10
      }
    ]
  },
  {
    "order_id": 12,
    "distributor_code": 3000,
    "order_date": "2004-04-23",
    "payment_date": "2004-05-11",
    "contents": [
      {
        "good_code": 411,
        "good_name": "Колонки газові Gorenje 13л/ хв.",
        "price": 120,
        "quantity": 26
      },
      {
        "good_code": 511,
        "good_name": "Колонки газові Bayard 16л/ хв.",
        "price": 160,
        "quantity": 21
      }
    ]
  }
]


db.distributors.drop()
db.orders.drop()
db.distributors.insert_many(distributors)
db.orders.insert_many(orders)

print("Колекції успішно створені!")
print(f"distributors: {db.distributors.count_documents({})} документів")
print(f"orders: {db.orders.count_documents({})} документів")