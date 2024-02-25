document.addEventListener('DOMContentLoaded', (event) => {
    const menuToggle = document.getElementById('menu-toggle');
    const menuItems = document.getElementById('menu-items');

    // Explicitly set the initial display style of menuItems to 'none'
    menuItems.style.display = 'none';

    menuToggle.addEventListener('click', (event) => {
        menuItems.style.display = menuItems.style.display === 'none' ? 'block' : 'none';
    });
});