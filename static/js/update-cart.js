//updating cart on Add to cart button click
var buttons = document.getElementsByClassName("update-cart")
var quantity = document.getElementById("quantity")
for (let index = 0; index < buttons.length; index++) {
    buttons[index].addEventListener('click', function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        
        if (user === "AnonymousUser"){
            window.location.href = "/account/register/";
        }
        else{
            updateUserCart(productId,action,index)
        }
    })
}

function updateUserCart(productId,action,index){
    var url = "/ecom/updateItem/";

    fetch (url,{
        method : 'POST',
        headers : {
            'content-type' : 'application/json',
            'X-CSRFToken' : csrftoken
        },
        body : JSON.stringify({'productId':productId,'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:',data)
        if (data=="Item is updated") {
            if(page=="cart"){

                if (action=="add"){
                    location.reload()
                }else if (action=="remove"){
                    location.reload()
                }
                
            }else{
                buttons[index].innerHTML = "&#10003; Added to Cart";
                buttons[index].dataset.action = "removeItem";
            }
        }
        else if(data=="Item is removed"){
            if (page=="cart"){
                location.reload()
            }else{
                buttons[index].innerHTML = "Add to Cart";
                buttons[index].dataset.action = "add";
            }
        }
        else{
            alert("Something went wrong... Please try again");
        }
        
    })    
}

