import grpc
from concurrent import futures
import time
import market_pb2
import market_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MarketServicer(market_pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = {}
        self.items = {}
        self.item_id_counter = 1
        self.wishlists = {}  
        self.ratings = {}  
        self.raters = {}

    def RegisterSeller(self, request, context):
        address = request.address
        uuid = request.uuid
        if address in self.sellers:
            return market_pb2.RegistrationResponse(message="FAIL")
        else:
            self.sellers[address] = uuid
            print(f"Seller join request from {address}, uuid = {uuid}")
            return market_pb2.RegistrationResponse(message="SUCCESS")

    def SellItem(self, request, context):
        item_name = request.name
        category = request.category
        quantity = request.quantity
        description = request.description
        seller_address = request.seller_address
        price = request.price
        seller_uuid = request.seller_uuid

        # Assign a unique ID to the item
        item_id = self.item_id_counter
        self.item_id_counter += 1

        # Store item details in the database or data structure
        self.items[item_id] = {
            'name': item_name,
            'category': category,
            'quantity': quantity,
            'description': description,
            'seller_address': seller_address,
            'price': price,
            'seller_uuid': seller_uuid
        }

        print(f"Item {item_id} added to the market by seller {seller_address}")

        return market_pb2.SellItemResponse(message="SUCCESS", item_id=item_id)

    def UpdateItem(self, request, context):
        item_id = request.item_id
        new_price = request.new_price
        new_quantity = request.new_quantity
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if item_id in self.items:
            item = self.items[item_id]
            if item['seller_address'] == seller_address and item['seller_uuid'] == seller_uuid:
                ratings = self.ratings.get(item_id, [])
                average_rating = sum(ratings) / len(ratings) if ratings else 0
                item['price'] = new_price
                item['quantity'] = new_quantity
                print(f"Item {item_id} updated by seller {seller_address}")
                
                        
                return market_pb2.UpdateItemResponse(message="SUCCESS")
            else:
                return market_pb2.UpdateItemResponse(message="FAILED: Unauthorized")
        else:
            return market_pb2.UpdateItemResponse(message="FAILED: Item not found")

    
    def DisplayItems(self, request, context):
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        for item_id, item in self.items.items():
            
            if item['seller_address'] == seller_address and item['seller_uuid'] == seller_uuid:
                ratings = self.ratings.get(item_id, [])
                average_rating = sum(ratings) / len(ratings) if ratings else 0
                yield market_pb2.ItemDetails(
                    item_id=item_id,
                    name=item['name'],
                    category=item['category'],
                    quantity=item['quantity'],
                    description=item['description'],
                    seller_address=item['seller_address'],
                    price=item['price'],
                    seller_uuid=item['seller_uuid'],
                    rating=average_rating
                )
    
    def SearchItem(self, request, context):
    # If item_name and category are both given, return items that match both
        if request.item_name and request.category != "ANY":
            for item_id, item in self.items.items():
                if item['name'] == request.item_name and item['category'] == request.category:
                    yield market_pb2.ItemDetails(
                        item_id=item_id,
                        name=item['name'],
                        category=item['category'],
                        quantity=item['quantity'],
                        description=item['description'],
                        seller_address=item['seller_address'],
                        price=item['price'],
                        seller_uuid=item['seller_uuid']
                    )

        # If only category is given, return all items in that category
        elif request.item_name == "" and request.category != "ANY":
            for item_id, item in self.items.items():
                if item['category'] == request.category:
                    yield market_pb2.ItemDetails(
                        item_id=item_id,
                        name=item['name'],
                        category=item['category'],
                        quantity=item['quantity'],
                        description=item['description'],
                        seller_address=item['seller_address'],
                        price=item['price'],
                        seller_uuid=item['seller_uuid']
                    )

        # If item_name is empty and category is ANY, return all items
        elif request.item_name == "" and request.category == "ANY":
            for item_id, item in self.items.items():
                yield market_pb2.ItemDetails(
                    item_id=item_id,
                    name=item['name'],
                    category=item['category'],
                    quantity=item['quantity'],
                    description=item['description'],
                    seller_address=item['seller_address'],
                    price=item['price'],
                    seller_uuid=item['seller_uuid']
                )
   
        
    def DeleteItem(self, request, context):
        item_id = request.item_id
        seller_address = request.seller_address
        seller_uuid = request.seller_uuid

        if item_id in self.items:
            item = self.items[item_id]
            if item['seller_address'] == seller_address and item['seller_uuid'] == seller_uuid:
                del self.items[item_id]
                print(f"Item {item_id} deleted by seller {seller_address}")
                return market_pb2.DeleteItemResponse(message="SUCCESS")
            else:
                return market_pb2.DeleteItemResponse(message="FAILED: Unauthorized")
        else:
            return market_pb2.DeleteItemResponse(message="FAILED: Item not found")
        

    def BuyItem(self, request, context):
        if request.item_id in self.items and self.items[request.item_id]['quantity'] >= request.quantity:
            # Reduce quantity of the item
            self.items[request.item_id]['quantity'] -= request.quantity
            
            # self.send_notification_to_seller(request.seller_address, purchase_notification)
            return market_pb2.SellItemResponse(message="SUCCESS", item_id=request.item_id)
        else:
            return market_pb2.SellItemResponse(message="FAILED: Item not available or quantity insufficient")


    def AddToWishList(self, request, context):
        if request.item_id in self.items:
            # Add item to buyer's wishlist
            if request.buyer_address not in self.wishlists:
                self.wishlists[request.buyer_address] = []
            self.wishlists[request.buyer_address].append(request.item_id)
            return market_pb2.RegistrationResponse(message="SUCCESS")
        else:
            return market_pb2.RegistrationResponse(message="FAILED: Item not found")

    def RateItem(self, request, context):
        if request.item_id in self.items:
            # Check if the buyer has already rated this item
            if request.buyer_address in self.raters.get(request.item_id, []):
                return market_pb2.RateItemResponse(message="FAILED: You have already rated this item")
            
            # Add rating for item
            if request.item_id not in self.ratings:
                self.ratings[request.item_id] = []
            self.ratings[request.item_id].append(request.rating)

            # Add buyer to the list of raters for this item
            if request.item_id not in self.raters:
                self.raters[request.item_id] = []
            self.raters[request.item_id].append(request.buyer_address)

            return market_pb2.RateItemResponse(message="SUCCESS")
        else:
            return market_pb2.RateItemResponse(message="FAILED: Item not found")
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market server started on port 50051")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
