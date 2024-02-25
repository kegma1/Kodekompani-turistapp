
document.addEventListener('DOMContentLoaded', (event) => {
    const toggleButton = document.querySelector('.menu-toggle');
    const menuItems = document.querySelector('.menu-items');

    toggleButton.addEventListener('click', () => {
        menuItems.style.display = menuItems.style.display === 'block' ? 'none' : 'block';
    });
});
