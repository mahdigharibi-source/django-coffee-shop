
const addressData = document.getElementById("address-data");
console.log('1')
const urls = {
    default: addressData.dataset.setDefaultUrl,
    delete: addressData.dataset.deleteAddressUrl,
};
console.log('2')
console.log(urls.default)
const csrfToken = addressData.dataset.csrfToken;
function setDefaultAddress(address_id) {
    $.ajax({
        url: urls.default,
        method: 'POST',
        data: {
            address_id: address_id,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {
            location.reload();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}


function deleteAddress(address_id) {
    $.ajax({
        url: urls.delete,
        method: 'POST',
        data: {
            address_id: address_id,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {
            location.reload();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}