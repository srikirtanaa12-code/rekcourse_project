const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');

document.getElementById('showSignup').addEventListener('click', function(e) {
    e.preventDefault();
    loginForm.classList.remove('active');
    loginForm.classList.add('hidden');
    signupForm.classList.remove('hidden');
    signupForm.classList.add('active');
});

document.getElementById('showLogin').addEventListener('click', function(e) {
    e.preventDefault();
    signupForm.classList.remove('active');
    signupForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
    loginForm.classList.add('active');
});