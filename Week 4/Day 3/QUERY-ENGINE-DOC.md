# Query Engine Documentation

## Overview
The Query Engine manages:
- Filtering
- Searching
- Sorting
- Soft delete handling
- Inclusion of deleted records( using `includeDeleted=true`)

## 1- Get All Products

### Endpoint

`GET /products`

### Descripion
Returns only active products ( `where deletedAt = null`).

### Screenshot
![Products](./screenshots/productsListing.png)

---

## 2- Search Products


### Endpoint

`GET /products?search=iphone`

### Descripion
Searches products by name using case-insensitive matching.

### Example Behavior
- Matches partial names
- Ignores letter casing

### Screenshot
![Searching with min and max price](./screenshots/getSearchSort.png)

## 3- Sort Products


### Endpoint
- Ascending order: Sorts products by price in ascending order (lowest to highest).
`GET /products?sort=price&order=asc`
- Descending order:  Sorts products by price in descending order (highest to lowest).
`GET /products?sort=price&order=desc`


### Screenshot
![Sort-Ascending order](./screenshots/sortAsc.png)
![Sort-Descending order](./screenshots/sortDesc.png)

## 4- Soft Delete Product

### Endpoint

`DELETE /products/:id`

### Description
- Does not permanently delete the product.
- Sets `deletedAt` field to current timestamp.
- Product becomes hidden from normal `/products` request.

### Screenshot

![Products after soft delete](./screenshots/deleted.png)

## 5- Include Soft Deleted Products

### Endpoint

`GET /products?includeDeleted=true`

### Description

Returns:
- Active products
- Soft deleted products

### Screenshot

![Products with includeDeleted](./screenshots/includeDeletedTrue.png)




