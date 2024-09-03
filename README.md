<H1 align="center"> Distributed Shopping Platform </H1>

<p align="Left">
This project implements a distributed shopping platform using Google Cloud, gRPC, and Protocol Buffers. The platform simulates a central marketplace where buyers and sellers interact through a Market (central platform) without direct communication between each other. The system is designed to run on multiple virtual machine instances in Google Cloud, each representing a different node (Market, Buyer, Seller).
</p>

## `Components`
  <ul>
  <li>Market (Central Platform)</li>
  <li>Seller (Client)</li>
  <li>Buyer (Client)</li>
  </ul>

### `Market (Central Platform):`
The Market acts as the central hub, managing all seller and buyer interactions. It maintains seller accounts, product listings, transaction logs, reviews, and notifications. Sellers and buyers connect to the Market using a known IP:port combination.

### `Seller (Client):`
Each seller operates on a unique address and interacts with the Market to manage their inventory and sales. Sellers can register, add, update, delete, and view their products on the Market. They also receive notifications for any transactions related to their products.

### `Buyer (Client):`
Buyers interact with the Market to search for products, make purchases, wishlist items, and rate products. Buyers also receive notifications about updates to their wishlisted items.

## `gRPC Implementation`
  <ul>
  <li>Seller ↦ Market</li>
  <li>Buyer ↦ Market</li>
  <li>Market ↦ Buyer/Seller</li>
  </ul>

### `Seller ↦ Market:`
- **RegisterSeller**: Sellers register with the Market by providing their IP:port and a UUID. The Market responds with SUCCESS or FAIL.
- **SellItem**: Sellers post new items on the Market, including details like product name, category, quantity, and price. The Market assigns a unique item ID and responds with SUCCESS, FAIL, or the item ID.
- **UpdateItem**: Sellers update item details on the Market. Successful updates trigger notifications to interested buyers.
- **DeleteItem**: Sellers delete items from the Market.
- **DisplaySellerItems**: Sellers can view all their listed items, including detailed information.

### `Buyer ↦ Market:`
- **SearchItem**: Buyers search for items by name or category. The Market returns a list of matching items.
- **BuyItem**: Buyers purchase items from the Market, which automatically updates the item quantity and triggers notifications to the seller.
- **AddToWishList**: Buyers add items to their wishlist to receive notifications on updates.
- **RateItem**: Buyers rate items, which updates the Market's records.

### `Market ↦ Buyer/Seller:`
- **NotifyClient**: The Market sends notifications to buyers and sellers about updates to items they are interested in or have listed.


## `License`
MIT © Atharv Srivastava 2024<br/>

<p align="Left"> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: </p> <p align="Left"> The above copyright notice and this permission notice shall be included in all copies or substantial 
    portions of the Software. </p> <p align="Left"> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
      DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. </p> <p align="center"> --- EOF --- </p> 
