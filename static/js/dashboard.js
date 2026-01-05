const ctx = document.getElementById('bookingChart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Bookings',
            data: [5, 8, 6, 10, 12, 9, 7],
            backgroundColor: '#0a66c2'
        }]
    }
});
