
function showPopup(popupId) {
    document.getElementById(popupId).classList.add('visible');
}

function hidePopup(popupId) {
    document.getElementById(popupId).classList.remove('visible');
}

function showUpdatePopup(id, train_no, train_name, date, route) {
    document.getElementById('update-train-id').value = id;
    document.getElementById('update-train-no').value = train_no;
    document.getElementById('update-train-name').value = train_name;
    document.getElementById('update-train-date').value = date;
    document.getElementById('update-route').value = route;
    showPopup('update-popup-form');
}


