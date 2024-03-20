document.addEventListener('DOMContentLoaded', function () {
    let buyNowButton = document.getElementById('buyNowButton');
    let buyNowDropdown = document.getElementById('buyNowDropdown');

    buyNowButton.addEventListener('click', function () {
        if (buyNowDropdown.style.display === 'none' || buyNowDropdown.style.display === '') {
            buyNowDropdown.style.display = 'block';
        } else {
            buyNowDropdown.style.display = 'none';
        }
    });
});
