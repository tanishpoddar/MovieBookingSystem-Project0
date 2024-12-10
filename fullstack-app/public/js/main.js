// main.js
document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const theaterSelect = document.getElementById('theater-select');
    const screenSelect = document.getElementById('screen-select');
    const seatsContainer = document.getElementById('seats-container');
    const foodContainer = document.getElementById('food-container');
    const customerName = document.getElementById('customer-name');
    const bookButton = document.getElementById('book-button');
    const bookingSummary = document.getElementById('booking-summary');
    const summaryContent = document.getElementById('summary-content');

    // Modal elements
    const cancelModal = document.getElementById('cancel-modal');
    const cancelTicketBtn = document.getElementById('cancel-ticket-btn');
    const cancelConfirmBtn = document.getElementById('cancel-confirm-btn');
    const cancelCloseBtn = document.getElementById('cancel-close-btn');
    const bookingIdInput = document.getElementById('booking-id');

    let selectedSeat = null;
    let selectedScreen = null;

    // Load theaters
    fetch('/api/theaters')
        .then(response => response.json())
        .then(theaters => {
            theaters.forEach(theater => {
                const option = document.createElement('option');
                option.value = theater.id;
                option.textContent = `${theater.name} - ${theater.location}`;
                theaterSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading theaters:', error);
            alert('Failed to load theaters. Please refresh the page.');
        });

    // Load food items
    fetch('/api/food-items')
        .then(response => response.json())
        .then(foodItems => {
            foodItems.forEach(item => {
                const div = document.createElement('div');
                div.className = 'food-item';
                div.innerHTML = `
                    <span>${item.name} - Rs. ${item.price}</span>
                    <input type="number" min="0" value="0" data-id="${item.id}" data-price="${item.price}">
                `;
                foodContainer.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Error loading food items:', error);
            alert('Failed to load food items. Please refresh the page.');
        });

    // Theater selection change handler
    theaterSelect.addEventListener('change', (e) => {
        const theaterId = e.target.value;
        screenSelect.innerHTML = '<option value="">Choose a screen</option>';
        screenSelect.disabled = !theaterId;
        seatsContainer.innerHTML = '';
        selectedScreen = null;
        selectedSeat = null;
        
        if (theaterId) {
            fetch(`/api/theaters/${theaterId}/screens`)
                .then(response => response.json())
                .then(screens => {
                    screens.forEach(screen => {
                        const option = document.createElement('option');
                        option.value = screen.id;
                        option.textContent = `${screen.screen_type} - Rs. ${screen.price}`;
                        option.dataset.type = screen.screen_type;
                        option.dataset.price = screen.price;
                        screenSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error loading screens:', error);
                    alert('Failed to load screens. Please try again.');
                });
        }
    });

    // Screen selection change handler
    screenSelect.addEventListener('change', (e) => {
        const screenId = e.target.value;
        selectedScreen = screenId ? {
            id: screenId,
            type: e.target.selectedOptions[0].dataset.type,
            price: parseFloat(e.target.selectedOptions[0].dataset.price)
        } : null;
        
        seatsContainer.innerHTML = '';
        selectedSeat = null;
        
        // In main.js, in the screen selection change handler
        if (screenId) {
            fetch(`/api/screens/${screenId}/seats`)
                .then(response => response.json())
                .then(seats => {
                    seats.forEach(seat => {
                        const div = document.createElement('div');
                        div.className = `seat ${seat.is_booked ? 'booked' : ''}`;
                        div.textContent = seat.seat_number;
                        div.dataset.id = seat.id;
                        
                        // Allow clicking even on booked seats!
                        div.addEventListener('click', () => {
                            document.querySelectorAll('.seat').forEach(s => s.classList.remove('selected'));
                            div.classList.add('selected');
                            selectedSeat = seat;
                        });
                        
                        seatsContainer.appendChild(div);
                    });
                })
                .catch(error => {
                    console.error('Error loading seats:', error);
                    alert('Failed to load seats. Please try again.');
                });
            }
    });

// Booking handler
bookButton.addEventListener('click', () => {
    console.log('Starting booking process...'); // Debug log
    
    if (!selectedScreen || !selectedSeat || !customerName.value.trim()) {
        alert('Please select a screen, seat, and enter your name');
        return;
    }

    // Collect food orders
    const foodOrders = Array.from(foodContainer.querySelectorAll('input'))
        .map(input => ({
            foodItemId: parseInt(input.dataset.id),
            quantity: parseInt(input.value),
            price: parseFloat(input.dataset.price)
        }))
        .filter(order => order.quantity > 0);

    // Create booking
    fetch('/api/bookings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            screenId: selectedScreen.id,
            seatId: selectedSeat.id,
            customerName: customerName.value.trim(),
            foodOrders,
            screenType: selectedScreen.type
        })
    })
    .then(response => response.json())
    .then(booking => {
        if (booking.success) {
            let summaryHTML = '';
            
            if (booking.isWaitingList) {
                // Waiting list booking summary
                summaryHTML = `
                    <p><strong>Booking Status:</strong> Waiting List</p>
                    <p><strong>Waiting List Position:</strong> ${booking.waitingListPosition}</p>
                    <p><strong>Customer Name:</strong> ${customerName.value}</p>
                    <p><strong>Screen Type:</strong> ${selectedScreen.type}</p>
                    <p class="note">You will be automatically upgraded to a confirmed booking when a seat becomes available.</p>
                `;
            } else {
                // Calculate food total with discount
                let foodDiscount = selectedScreen.type === 'Gold' ? 0.10 : 
                                 selectedScreen.type === 'Max' ? 0.05 : 0;
                
                let foodTotal = foodOrders.reduce((total, order) => 
                    total + (order.price * order.quantity * (1 - foodDiscount)), 0);

                // Regular booking summary
                summaryHTML = `
                    <p><strong>Booking Status:</strong> Confirmed</p>
                    <p><strong>Booking ID:</strong> ${booking.bookingId}</p>
                    <p><strong>Customer Name:</strong> ${customerName.value}</p>
                    <p><strong>Screen Type:</strong> ${selectedScreen.type}</p>
                    <p><strong>Ticket Price:</strong> Rs. ${selectedScreen.price}</p>
                    <p><strong>Food & Beverages:</strong> Rs. ${foodTotal.toFixed(2)}</p>
                    <p><strong>Total Amount:</strong> Rs. ${booking.totalAmount.toFixed(2)}</p>
                `;
            }
            
            // Display the summary
            summaryContent.innerHTML = summaryHTML;
            bookingSummary.style.display = 'block';

            // Reset form
            theaterSelect.value = '';
            screenSelect.value = '';
            screenSelect.disabled = true;
            seatsContainer.innerHTML = '';
            customerName.value = '';
            foodContainer.querySelectorAll('input').forEach(input => input.value = 0);
            selectedSeat = null;
            selectedScreen = null;
        } else {
            alert('Booking failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Booking error:', error);
        alert('Booking failed. Please try again.');
    });
});

    // Cancel ticket button handler
    cancelTicketBtn.addEventListener('click', () => {
        cancelModal.classList.add('active');
    });

    // Cancel confirmation handler
    cancelConfirmBtn.addEventListener('click', () => {
        const bookingId = bookingIdInput.value.trim();
        if (!bookingId) {
            alert('Please enter a booking ID');
            return;
        }

        fetch(`/api/bookings/${bookingId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                let message = 'Ticket cancelled successfully.';
                if (result.waitingListProcessed) {
                    message += ` A waiting list booking has been confirmed (New Booking ID: ${result.newBookingId}).`;
                }
                alert(message);
                cancelModal.classList.remove('active');
                bookingIdInput.value = '';
                bookingSummary.style.display = 'none';
            } else {
                alert(result.error || 'Failed to cancel ticket');
            }
        })
        .catch(error => {
            console.error('Cancellation error:', error);
            alert('Failed to cancel ticket. Please try again.');
        });
    });

    // Close modal button handler
    cancelCloseBtn.addEventListener('click', () => {
        cancelModal.classList.remove('active');
        bookingIdInput.value = '';
    });

    // Close modal when clicking outside
    cancelModal.addEventListener('click', (e) => {
        if (e.target === cancelModal) {
            cancelModal.classList.remove('active');
            bookingIdInput.value = '';
        }
    });
});