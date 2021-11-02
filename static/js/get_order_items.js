
//checking for the items whether they are added to cart
var buttons = document.getElementsByClassName("update-cart")
var OrderItemUrl = "/ecom/all_order_items/";

fetch (OrderItemUrl,{
    method : 'GET',
    headers : {
        'X-CSRFToken' : csrftoken
    }
})

.then((response) => {
    return response.json()
})

.then((data) => {
    if (data.status == "200 OK"){
        for (let i of data.order_items_ids){
            // console.log(i-1)
            buttons[i-1].innerHTML = "&#10003; Added to Cart";
            buttons[i-1].dataset.action = "removeItem";
            // buttons[i-1].classList.remove("update-cart");
        }
    }
})  