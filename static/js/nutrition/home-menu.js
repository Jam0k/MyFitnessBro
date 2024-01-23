function showSubMenu(subMenuId, currentBtnId) {
    // Hide all primary buttons
    document.getElementById('btnFood').style.display = 'none';
    document.getElementById('btnMeals').style.display = 'none';

    // Show the sub menu
    document.getElementById(subMenuId).style.display = 'block';
}

function hideSubMenu(subMenuId) {
    // Show all primary buttons
    document.getElementById('btnFood').style.display = 'block';
    document.getElementById('btnMeals').style.display = 'block';

    // Hide the sub menu
    document.getElementById(subMenuId).style.display = 'none';
}