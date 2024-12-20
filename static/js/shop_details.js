function showUpdatePopup(id, name, username, shopName, address) {
    document.getElementById('update-shop-id').value = id;
    document.getElementById('update-name').value = name;
    document.getElementById('update-username').value = username;
    document.getElementById('update-shop-name').value = shopName;
    document.getElementById('update-address').value = address;
    document.getElementById('update-popup-form').style.display = 'block';
}

function hidePopup(popupId) {
    document.getElementById(popupId).style.display = 'none';
}