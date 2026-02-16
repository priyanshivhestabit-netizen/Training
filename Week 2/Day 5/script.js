const productContainer = document.getElementById("productContainer");
const searchInput = document.getElementById("searchInput");
const sortSelect = document.getElementById("sortSelect");

let products=[];

async function fetchProducts(){
    try{
        const response = await fetch("https://dummyjson.com/products");
        const data = await response.json();
        products=data.products;
        renderProducts(products);
    }
    catch(error){
        productContainer.innerHTML = "<p>Failed to load products</p>";
        console.error("error fetching products:", error);
    }
}

function renderProducts(productArray){
    productContainer.innerHTML="";

    productArray.forEach(product => {
        const card =document.createElement("div");
        card.classList.add("card");

        card.innerHTML= `
            <img src="${product.thumbnail}" alt="${product.title}" />
            <h3>${product.title}</h3>
            <p class="price">$${product.price}</p>
        `;

        productContainer.appendChild(card);
    });
}

//search 
searchInput.addEventListener("input",() => {
    const searchValue = searchInput.value.toLowerCase();

    const filteredProducts = products.filter( product => 
        product.title.toLowerCase().includes(searchValue)
    );
    renderProducts(filteredProducts);
});

//sort
sortSelect.addEventListener("change",() => {
    const value=sortSelect.value;

    if(value==="high"){
        const sorted = [...products].sort((a,b)=>b.price - a.price);
        renderProducts(sorted);
    }
    else if(value==="low"){
        const sorted = [...products].sort((a,b)=>a.price - b.price);
        renderProducts(sorted);
    }
    else{
        renderProducts(products);
    }
});

fetchProducts();