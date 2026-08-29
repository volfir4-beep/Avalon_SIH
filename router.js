// This file acts as your frontend router to direct users to your friend's page
document.addEventListener("DOMContentLoaded", () => {
    const loginButton = document.getElementById('loginRouteBtn');

    if (loginButton) {
        loginButton.addEventListener('click', () => {
            // Replace 'login.html' with the actual filename your friend creates
            window.location.href = 'login.html'; 
        });
    }
});