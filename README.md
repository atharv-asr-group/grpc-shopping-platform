# Distributed Shopping Platform

This project implements a distributed shopping platform using **gRPC** and **Protocol Buffers**. It simulates a central marketplace where buyers and sellers interact through a Market (central platform) without direct communication between each other. The system is designed to run on multiple nodes, each representing a different role (Market, Buyer, Seller).

## Features

- **Market (Central Platform):**
  - Acts as the central hub for managing interactions between buyers and sellers.
  - Maintains seller accounts, product listings, transaction logs, reviews, and notifications.

- **Seller (Client):**
  - Allows sellers to register, add, update, delete, and view their products.
  - Sellers receive notifications for transactions related to their products.

- **Buyer (Client):**
  - Enables buyers to search for products, make purchases, wishlist items, and rate products.
  - Buyers receive notifications about updates to their wishlisted items.

## Project Structure

```
.
├── [`buyer.py`](buyer.py )               # Buyer client implementation
├── [`seller.py`](seller.py )              # Seller client implementation
├── [`market_server.py`](market_server.py )       # Market server implementation
├── [`market.proto`](market.proto )           # Protocol Buffers definition
├── [`market_pb2.py`](market_pb2.py )          # Generated Python code from [`market.proto`](market.proto )
├── [`market_pb2_grpc.py`](market_pb2_grpc.py )     # Generated gRPC code from [`market.proto`](market.proto )
├── [`README.md`](README.md )              # Project documentation
└── __pycache__/           # Compiled Python files
```

## Components

### 1. **Market (Central Platform)**
The Market server manages all interactions between buyers and sellers. It provides the following functionalities:
- **Seller Operations:**
  - Register sellers.
  - Add, update, delete, and display items.
- **Buyer Operations:**
  - Search for items.
  - Buy items.
  - Add items to a wishlist.
  - Rate items.
- **Notifications:**
  - Notify sellers about purchases.
  - Notify buyers about updates to wishlisted items.

### 2. **Seller (Client)**
The seller client interacts with the Market to:
- Register as a seller.
- Add new items for sale.
- Update or delete existing items.
- View all listed items.

### 3. **Buyer (Client)**
The buyer client interacts with the Market to:
- Search for items by name or category.
- Purchase items.
- Add items to a wishlist.
- Rate purchased items.

## gRPC API

The project uses **gRPC** for communication between the Market, Buyer, and Seller. The API is defined in the [`market.proto`](market.proto) file. Key RPC methods include:

### Seller ↔ Market
- **RegisterSeller**: Register a seller with the Market.
- **SellItem**: Add a new item to the Market.
- **UpdateItem**: Update item details.
- **DeleteItem**: Remove an item from the Market.
- **DisplayItems**: View all items listed by the seller.

### Buyer ↔ Market
- **SearchItem**: Search for items by name or category.
- **BuyItem**: Purchase an item.
- **AddToWishList**: Add an item to the buyer's wishlist.
- **RateItem**: Rate an item.

### Notifications
- The Market sends notifications to buyers and sellers about updates to items they are interested in or have listed.

## How to Run

1. **Start the Market Server:**
   Run the `market_server.py` file to start the Market server.
   ```bash
   python market_server.py
   ```

2. **Run the Seller Client:**
   Use the `seller.py` file to interact with the Market as a seller.
   ```bash
   python seller.py
   ```

3. **Run the Buyer Client:**
   Use the `buyer.py` file to interact with the Market as a buyer.
   ```bash
   python buyer.py
   ```

## Dependencies

- Python 3.8+
- gRPC
- Protocol Buffers

Install the required dependencies using:
```bash
pip install grpcio grpcio-tools
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author:** Atharv Srivastava
