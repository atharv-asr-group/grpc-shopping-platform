import grpc
import market_pb2
import market_pb2_grpc
import uuid
import random

class SellerClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('10.190.0.2:50051')
        self.stub = market_pb2_grpc.MarketStub(self.channel)
        self.seller_uuid = str(uuid.uuid1())
        self.port = random.randint(3000, 4000)
        self.seller_address = f"10.190.0.3:{self.port}"   
            
    def register_seller(self):
        response = self.stub.RegisterSeller(market_pb2.RegistrationRequest(address=self.seller_address, uuid=self.seller_uuid))
        print("Response received:", response.message)

    def sell_item(self, name, category, quantity, description, price):
        response = self.stub.SellItem(market_pb2.SellItemRequest(
            name=name,
            category=category,
            quantity=quantity,
            description=description,
            seller_address=self.seller_address,
            price=price,
            seller_uuid=self.seller_uuid
        ))
        print("Response received:", response.message)
        if response.message == "SUCCESS":
            print("Item ID:", response.item_id)

    def update_item(self, item_id, new_price, new_quantity):
        response = self.stub.UpdateItem(market_pb2.UpdateItemRequest(
            item_id=item_id,
            new_price=new_price,
            new_quantity=new_quantity,
            seller_address=self.seller_address,
            seller_uuid=self.seller_uuid
        ))
        print("Response received:", response.message)

    def display_items(self):
        for item in self.stub.DisplayItems(market_pb2.DisplayItemsRequest(
            seller_address=self.seller_address,
            seller_uuid=self.seller_uuid
        )):
            print(f"Item ID: {item.item_id}, Name: {item.name}, Category: {item.category}, Quantity: {item.quantity}, Price: {item.price} , Rating:{item.rating}")

    def delete_item(self, item_id):
        response = self.stub.DeleteItem(market_pb2.DeleteItemRequest(
            item_id=item_id,
            seller_address=self.seller_address,
            seller_uuid=self.seller_uuid
        ))
        print("Response received:", response.message)

if __name__ == '__main__':
    seller_client = SellerClient()
    
    while True:
        print("\nMenu:")
        print("1. Register Seller")
        print("2. Sell/Add Item")
        print("3. Update Item")
        print("4. Display Items")
        print("5. Delete Item")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            seller_client.register_seller()
        elif choice == "2":
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            quantity = int(input("Enter item quantity: "))
            description = input("Enter item description: ")
            price = float(input("Enter item price: "))
            seller_client.sell_item(name, category, quantity, description, price)
        elif choice == "3":
            item_id = int(input("Enter item ID to update: "))
            new_price = float(input("Enter new price: "))
            new_quantity = int(input("Enter new quantity: "))
            seller_client.update_item(item_id, new_price, new_quantity)
        elif choice == "4":
            seller_client.display_items()
        elif choice == "5":
            item_id = int(input("Enter item ID to delete: "))
            seller_client.delete_item(item_id)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
