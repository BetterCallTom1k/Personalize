from db.db_client import db

def main():
    print("✅ Подключение к MongoDB успешно!")
    print("Коллекции:", db.list_collection_names())

if __name__ == "__main__":
    main()
