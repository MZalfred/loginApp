document.getElementById('signInOutForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const userAction = document.getElementById('userAction').value; // 'sign-in' or 'sign-out'

    toggleButtonState(userAction);

    // AJAX call to send data to server (using Fetch API)
    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&action=${userAction}`
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});

function toggleButtonState(userAction) {
    // Enabling/Disabling Buttons Based on Action
    const signInButton = document.getElementById('signInButton');
    const signOutButton = document.getElementById('signOutButton');
    const startBreakButton = document.getElementById('startBreak');
    const endBreakButton = document.getElementById('endBreak');

    if (userAction === 'sign-in') {
        signInButton.disabled = true;
        signOutButton.disabled = false;
        startBreakButton.disabled = false;
        endBreakButton.disabled = true;
    } else { // sign-out
        signInButton.disabled = false;
        signOutButton.disabled = true;
        startBreakButton.disabled = true;
        endBreakButton.disabled = true;
    }
}

function fetchReport() {
    // ... (existing fetchReport function)
}
