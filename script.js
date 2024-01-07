document.getElementById('signInOutForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const userAction = document.getElementById('userAction').value; // 'sign-in' or 'sign-out'

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

    // TODO: AJAX call to send data to server
    // Example AJAX call (uncomment and modify as needed):
    /*
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/login", true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send("username=" + encodeURIComponent(username) + "&action=" + userAction);
    */
});

function fetchActivityReport() {
    // Fetch and display the activity report
    // Placeholder function - expand with actual AJAX request
}

document.getElementById('signInOutForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Handle the sign-in or sign-out action
    // Placeholder - expand with actual form handling logic
});
