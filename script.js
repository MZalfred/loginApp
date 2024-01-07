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
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const url = `http://127.0.0.1:5000/fetch-logs?start=${startDate}&end=${endDate}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('reportTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = ''; // Clear existing data

            data.forEach(row => {
                let tr = `<tr>
                    <td>${row.user_id}</td>
                    <td>${row.action}</td>
                    <td>${row.timestamp}</td>
                </tr>`;
                tableBody.innerHTML += tr;
            });
        })
        .catch(error => console.error('Error:', error));
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(registration => {
        console.log('Service Worker registered with scope:', registration.scope);
      })
      .catch(error => {
        console.log('Service Worker registration failed:', error);
      });
  }

