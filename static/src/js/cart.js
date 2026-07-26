const cartData = document.getElementById("cart-data");

const urls = {
    increase: cartData.dataset.increaseUrl,
    decrease: cartData.dataset.decreaseUrl,
    remove: cartData.dataset.removeUrl,
    order: cartData.dataset.addToOrderUrl,

    cart: cartData.dataset.addToCartUrl,
    favorite: cartData.dataset.addToFavoriteUrl,
    login: cartData.dataset.loginUrl,
};

const csrfToken = cartData.dataset.csrfToken;
console.log(cartData);
console.log(urls);

function removeProduct(product_id) {
    $.ajax({
        url: urls.remove,
        method: 'POST',
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken

        },
        success: function (response) {
            console.log(response);
            window.location.reload();
            // do something with the response data
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            // handle the error case
        }
    });
}


function increaseProduct(product_id) {
    $.ajax({
        url: urls.increase,
        method: 'POST',
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken

        },
        success: function (response) {
            console.log(response);
            window.location.reload();
            // do something with the response data
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            // handle the error case
        }
    });
}

function decreaseProduct(product_id) {
    $.ajax({
        url: urls.decrease,
        method: 'POST',
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken

        },
        success: function (response) {
            console.log(response);
            window.location.reload();
            // do something with the response data
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            // handle the error case
        }
    });
}

function addToOrderList() {
    $.ajax({
        url: urls.order,
        type: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },

        success: function (response) {
            if (response.status === "success") {
                window.location.href = response.redirect_url;
            }
        },

        error: function (xhr) {
            const response = xhr.responseJSON;

            if (response.redirect_url) {
                alert(response.message);
                window.location.href = response.redirect_url;
            } else {
                alert(response.message || "خطایی رخ داده است.");
            }
        }
    });
}

function addToCart(product_id) {
    $.ajax({
        url: urls.cart,
        method: 'POST',
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken

        },

        success: function (response) {
            setTimeout(() => {
                location.reload();
            }, 500);
        },


        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            // handle the error case
        }
    });
}

function addToFavorite(product_id) {
    $.ajax({
        url: urls.favorite,
        method: 'POST',
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: csrfToken
        },

        success: function (data) {
            console.log('favorite')
            const button = document.getElementById(`favorite-${product_id}`);
            if (data.is_favorite) {
                button.classList.add("active")
            } else {
                button.classList.remove("active")
            }
        },

        error: function (xhr) {

            if (xhr.status === 401) {
                window.location.href = `${urls.login}?next=${encodeURIComponent(urls.next)}`;
            }
        }
    });
}

window.addEventListener("pageshow", function (event) {
    const navigation = performance.getEntriesByType("navigation")[0];

    if (event.persisted || navigation?.type === "back_forward") {
        location.reload();
    }
});
