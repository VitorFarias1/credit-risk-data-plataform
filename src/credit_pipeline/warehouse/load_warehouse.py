from credit_pipeline.warehouse.database import get_connection
from credit_pipeline.warehouse.loader import WarehouseLoader


def main():

    print("Loading Warehouse...")

    connection = get_connection()

    loader = WarehouseLoader(connection)

    loader.create_schemas()

    loader.load_trusted_table()

    connection.close()

    print("Warehouse Loaded.")


if __name__ == "__main__":
    main()