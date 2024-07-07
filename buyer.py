import grpc
import market_pb2
import market_pb2_grpc
import random

class BuyerClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('10.190.0.2:50051')
        self.stub = market_pb2_grpc.MarketStub(self.channel)
        self.port = random.randint(1000, 2000)
        self.buyer_address = f"10.190.0.4:{self.port}"
        # self.buyer_address = "ip:port"
            
    def add_to_wishlist(self, item_id):
        request = market_pb2.AddToWishListRequest(item_id=item_id, buyer_address=self.buyer_address)
        response = self.stub.AddToWishList(request)
        print("Response received:", response.message)

    def search_item(self, item_name, category):
        request = market_pb2.SearchItemRequest(item_name=item_name, category=category)
        responses = self.stub.SearchItem(request)
        for response in responses:
            print(f"Item ID: {response.item_id}, Name: {response.name}, Category: {response.category}, Quantity: {response.quantity}, Price: {response.price}")

            
    
    def buy_item(self, item_id, quantity):
        request = market_pb2.BuyItemRequest(item_id=item_id, quantity=quantity, buyer_address=self.buyer_address)
        response = self.stub.BuyItem(request)
        print("Response received:", response.message)
        if response.message == "SUCCESS":
            print("Item ID:", response.item_id)


    def rate_item(self, item_id, rating):
        request = market_pb2.RateItemRequest(item_id=item_id, rating=rating, buyer_address=self.buyer_address)
        response = self.stub.RateItem(request)
        print("Response received:", response.message)

if __name__ == '__main__':
    buyer_client = BuyerClient()
    
    while True:
        print("\nMenu:")
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            item_name = input("Enter item name (leave blank for all items): ")
            category = input("Enter item category (ANY/ELECTRONICS/FASHION/OTHERS): ")
            buyer_client.search_item(item_name, category)
        elif choice == "2":
            item_id = int(input("Enter item ID to buy: "))
            quantity = int(input("Enter quantity to buy: "))
            buyer_client.buy_item(item_id, quantity)
        elif choice == "3":
            item_id = int(input("Enter item ID to add to wishlist: "))
            buyer_client.add_to_wishlist(item_id)
        elif choice == "4":
            item_id = int(input("Enter item ID to rate: "))
            rating = int(input("Enter rating (0-5): "))
            buyer_client.rate_item(item_id, rating)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
