
/* ==============================
   DOM ELEMENTS (SAFE SELECTORS)
================================= */

/* ==============================
   DOM ELEMENTS (SAFE SELECTORS)
================================= */

const menuBtn = document.getElementById('menu-btn');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const notificationBtn = document.getElementById('notificationBtn');
const notificationDropdown = document.getElementById('notificationDropdown');
const ticketsModal = document.getElementById('bookedTicketsModal');
const accountModal = document.getElementById('accountModal');
const openTicketsModalBtn = document.getElementById('openTicketsModalBtn');
const openAccountModalBtn = document.getElementById('openAccountModalBtn');
const openTicketsModalBtnMobile = document.getElementById('openTicketsModalBtnMobile');
const openAccountModalBtnMobile = document.getElementById('openAccountModalBtnMobile');
const closeTicketsModalBtn = document.querySelector('#bookedTicketsModal .close-btn');
const closeAccountModalBtn = document.querySelector('.account-close');
const logoutBtn = document.getElementById('logoutBtn');
const logoutBtnMobile = document.getElementById('logoutBtnMobile');
const bookNowBtn = document.getElementById('bookNowBtn');



const confirmationModal = document.getElementById('confirmationModal');
const confirmYesBtn = document.getElementById('confirmYesBtn');
const confirmNoBtn = document.getElementById('confirmNoBtn');
const confirmationMessage = document.getElementById('confirmationMessage');
const logoutSuccessModal = document.getElementById('logoutSuccessModal');

let currentConfirmCallback = null;

/* ==============================
   SAFE BOOKINGS PARSE
================================= */

let userBookings = [];
try {
    const el = document.getElementById("bookings-data");
    if (el && el.textContent) {
        userBookings = JSON.parse(el.textContent) || [];
    }
} catch (err) {
    console.warn("Could not parse bookings-data:", err);
    userBookings = [];
}

/* ==============================
   SIDEBAR MENU
================================= */

if (menuBtn && sidebar && overlay) {
    menuBtn.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });
}

/* ==============================
   LOGOUT FLOW
================================= */

const logoutModal = document.getElementById('logoutModal');
const cancelLogoutBtn = document.getElementById('cancelLogoutBtn');
const confirmLogoutBtn = document.getElementById('confirmLogoutBtn');
const closeLogoutModalBtn = document.getElementById('closeLogoutModal');

if (logoutBtn && logoutModal) {
    logoutBtn.addEventListener("click", (e) => {
        e.preventDefault();
        sidebar.classList.remove('active'); // Close sidebar
        overlay.classList.remove('active');
        logoutModal.style.display = 'flex'; // Show styled modal
    });

    if (logoutBtnMobile) {
        logoutBtnMobile.addEventListener("click", (e) => {
            e.preventDefault();
            sidebar.classList.remove('active'); // Close sidebar
            overlay.classList.remove('active');
            logoutModal.style.display = 'flex'; // Show styled modal
        });
    }

    // Handle Cancel
    if (cancelLogoutBtn) {
        cancelLogoutBtn.addEventListener('click', () => {
            logoutModal.style.display = 'none';
        });
    }

    if (closeLogoutModalBtn) {
        closeLogoutModalBtn.addEventListener('click', () => {
            logoutModal.style.display = 'none';
        });
    }

    // Handle Confirm Logout
    if (confirmLogoutBtn) {
        confirmLogoutBtn.addEventListener('click', () => {
            // Perform Logout
            window.location.href = "/logout/";
        });
    }

    // Close on click outside
    window.addEventListener('click', (event) => {
        if (event.target === logoutModal) {
            logoutModal.style.display = 'none';
        }
    });
}

/* ==============================
   NOTIFICATIONS
================================= */



/* ==============================
   RENDER TICKETS MODAL
================================= */

function renderBookedTickets() {
    const listContainer = document.getElementById("bookedTicketsList");
    if (!listContainer) return;

    listContainer.innerHTML = "";

    if (!userBookings || userBookings.length === 0) {
        listContainer.innerHTML = `<p style="text-align:center;color:#c9a6ff;padding:40px;">
            No tickets booked yet.
        </p>`;
        return;
    }

    userBookings.forEach(b => {
        const item = document.createElement("div");
        item.className = "booking-item";
        item.id = `booking-${b.bookingId || b.id}`; // Add ID for easy removal

        const movie = b.movie || b.movie_name || "Unknown";
        const date = b.date || "";
        const time = b.time || "";
        const seats = b.seats || "";
        const id = b.bookingId || b.id || "";
        const ticketNumber = b.ticket_number || "N/A";

        item.innerHTML = `
            <div>
                <h4 style="color:#ffcc00;">${movie}</h4>
                <p style="color:#c9a6ff;">
                    🗓️ Date: ${date} at ${time}<br>
                    🪑 Seats: ${seats}<br>
                    🎫 Ticket: ${ticketNumber}<br>
                    #️⃣ ID: ${id}
                </p>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <a href="/download-ticket/${id}/" target="_blank" class="download-ticket-btn" style="flex: 1; text-align: center; padding: 10px; background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #1a1a2e; border: none; border-radius: 5px; text-decoration: none; font-weight: bold; cursor: pointer; transition: all 0.3s ease;">
                        <i class="fas fa-download"></i> Download Ticket
                    </a>
                    <form action="/cancel-my-booking/${id}/" method="POST" class="cancel-form" style="flex: 1;">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                        <button type="submit" class="cancel-btn" style="width: 100%; padding: 10px;">Cancel Booking</button>
                    </form>
                </div>
            </div>
        `;

        listContainer.appendChild(item);
    });
}

// Helper to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



// Initialize Page
document.addEventListener("DOMContentLoaded", () => {
    // 2. Initialize Notifications (Handled by notification.js)
    // renderNotifications(); // Removed: handled by notification.js

    // Check for Django messages and add to notifications
    const messages = document.querySelectorAll('.django-message');
    messages.forEach(msg => {
        // Use showNotification for Django messages (popups)
        const type = msg.dataset.tag || 'info'; // Assuming data-tag attribute or default
        showNotification(type, 'Notification', msg.textContent);
    });

    // 3. Initialize Modals & Event Listeners
    // Desktop navigation link
    if (openTicketsModalBtn && ticketsModal) {
        openTicketsModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            renderBookedTickets();
            ticketsModal.style.display = 'block';
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    // Mobile sidebar button
    if (openTicketsModalBtnMobile && ticketsModal) {
        openTicketsModalBtnMobile.addEventListener('click', () => {
            renderBookedTickets();
            ticketsModal.style.display = 'block';
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    if (closeTicketsModalBtn) {
        closeTicketsModalBtn.addEventListener('click', () => {
            ticketsModal.style.display = 'none';
        });
    }

    // Desktop navigation link
    if (openAccountModalBtn && accountModal) {
        openAccountModalBtn.addEventListener('click', (e) => {
            e.preventDefault();
            accountModal.style.display = 'block';
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    // Mobile sidebar button
    if (openAccountModalBtnMobile && accountModal) {
        openAccountModalBtnMobile.addEventListener('click', () => {
            accountModal.style.display = 'block';
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    if (closeAccountModalBtn) {
        closeAccountModalBtn.addEventListener('click', () => {
            accountModal.style.display = 'none';
        });
    }

    // Deposit Modal Logic
    const depositModal = document.getElementById('depositModal');
    const openDepositBtn = document.getElementById('openDepositModalBtn');
    const closeDepositBtn = document.getElementById('closeDepositModal');
    const depositForm = document.getElementById('depositForm');

    if (openDepositBtn && depositModal) {
        openDepositBtn.addEventListener('click', () => {
            depositModal.style.display = 'flex'; // Using flex as per homepage.html preference
            sidebar?.classList.remove('active');
            overlay?.classList.remove('active');
        });
    }

    if (closeDepositBtn && depositModal) {
        closeDepositBtn.addEventListener('click', () => {
            depositModal.style.display = 'none';
        });
    }

    if (depositForm) {
        depositForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(depositForm);
            try {
                const response = await fetch(depositForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                const data = await response.json();
                if (data.success) {
                    showNotification('success', 'Success', data.message);
                    const userBalance = document.getElementById('userBalance');
                    if (userBalance) userBalance.textContent = data.new_balance;
                    depositModal.style.display = "none";
                    depositForm.reset();
                } else {
                    showNotification('error', 'Error', data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('error', 'Error', "An error occurred. Please try again.");
            }
        });
    }

    window.addEventListener('click', (event) => {
        if (event.target === ticketsModal) ticketsModal.style.display = 'none';
        if (event.target === accountModal) accountModal.style.display = 'none';
        if (event.target === confirmationModal) confirmationModal.style.display = 'none';
        if (event.target === logoutSuccessModal) logoutSuccessModal.style.display = 'none';
        if (depositModal && event.target === depositModal) depositModal.style.display = 'none';
    });

    if (confirmYesBtn) {
        confirmYesBtn.addEventListener('click', () => {
            if (currentConfirmCallback) currentConfirmCallback();
        });
    }

    if (confirmNoBtn) {
        confirmNoBtn.addEventListener('click', () => {
            if (confirmationModal) confirmationModal.style.display = 'none';
            currentConfirmCallback = null;
        });
    }

    if (bookNowBtn) {
        bookNowBtn.addEventListener("click", () => {
            document.getElementById("movies").scrollIntoView({
                behavior: "smooth"
            });
        });
    }
});

/* ==============================
   HELPER
================================= */

function showNotification(type, title, message) {
    const modal = document.getElementById('notificationModal');
    const icon = document.getElementById('notificationIcon');
    const titleEl = document.getElementById('notificationTitle');
    const msgEl = document.getElementById('notificationMessage');
    const closeBtn = document.getElementById('closeNotificationBtn');

    if (!modal) return;

    titleEl.textContent = title;
    msgEl.textContent = message;

    // Reset classes
    icon.className = 'notification-icon';
    if (type === 'success') {
        icon.innerHTML = '<i class="fas fa-check-circle"></i>';
        icon.classList.add('success');
        titleEl.style.color = '#4caf50';
    } else if (type === 'error') {
        icon.innerHTML = '<i class="fas fa-times-circle"></i>';
        icon.classList.add('error');
        titleEl.style.color = '#ff4d4d';
    } else {
        icon.innerHTML = '<i class="fas fa-info-circle"></i>';
        icon.classList.add('info');
        titleEl.style.color = '#ffd700';
    }

    modal.style.display = 'flex'; // Flex to center

    if (closeBtn) {
        closeBtn.onclick = () => modal.style.display = 'none';
    }

    // Auto close after 3 seconds
    setTimeout(() => {
        modal.style.display = 'none';
    }, 3000);
}

function bookMovie(movieName) {
    localStorage.setItem("selectedMovie", movieName);
}

/* ==============================
   ACCOUNT MANAGEMENT MODALS
================================= */

// Get modal elements
const editProfileModal = document.getElementById('editProfileModal');
const changePasswordModal = document.getElementById('changePasswordModal');
const deleteAccountModal = document.getElementById('deleteAccountModal');

// Get button elements
const editAccountBtn = document.getElementById('editAccountBtn');
const changePasswordBtn = document.getElementById('changePasswordBtn');
const deleteAccountBtn = document.getElementById('deleteAccountBtn');

// Get close button elements
const closeEditProfile = document.getElementById('closeEditProfile');
const closeChangePassword = document.getElementById('closeChangePassword');
const closeDeleteAccount = document.getElementById('closeDeleteAccount');
const cancelDelete = document.getElementById('cancelDelete');

// Open Edit Profile Modal
if (editAccountBtn) {
    editAccountBtn.addEventListener('click', () => {
        editProfileModal.style.display = 'block';
        accountModal.style.display = 'none';
    });
}

// Open Change Password Modal
if (changePasswordBtn) {
    changePasswordBtn.addEventListener('click', () => {
        changePasswordModal.style.display = 'block';
        accountModal.style.display = 'none';
    });
}

// Open Delete Account Modal
if (deleteAccountBtn) {
    deleteAccountBtn.addEventListener('click', () => {
        deleteAccountModal.style.display = 'block';
        accountModal.style.display = 'none';
    });
}

// Close Edit Profile Modal
if (closeEditProfile) {
    closeEditProfile.addEventListener('click', () => {
        editProfileModal.style.display = 'none';
    });
}

// Close Change Password Modal
if (closeChangePassword) {
    closeChangePassword.addEventListener('click', () => {
        changePasswordModal.style.display = 'none';
    });
}

// Close Delete Account Modal
if (closeDeleteAccount) {
    closeDeleteAccount.addEventListener('click', () => {
        deleteAccountModal.style.display = 'none';
    });
}

// Cancel Delete
if (cancelDelete) {
    cancelDelete.addEventListener('click', () => {
        deleteAccountModal.style.display = 'none';
    });
}

// Close modals when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === editProfileModal) {
        editProfileModal.style.display = 'none';
    }
    if (event.target === changePasswordModal) {
        changePasswordModal.style.display = 'none';
    }
    if (event.target === deleteAccountModal) {
        deleteAccountModal.style.display = 'none';
    }
});

// Handle Edit Profile Form Submission
const editProfileForm = document.getElementById('editProfileForm');
if (editProfileForm) {
    editProfileForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(editProfileForm);

        try {
            const response = await fetch('/users/update-profile/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification('success', 'Success', 'Profile updated successfully!');
                editProfileModal.style.display = 'none';
                // Update displayed account info
                document.getElementById('accountFullName').textContent =
                    formData.get('first_name') + ' ' + formData.get('last_name');
                document.getElementById('accountEmail').textContent = formData.get('email');
                document.getElementById('accountPhone').textContent = formData.get('phone') || 'Not provided';
                const location = [formData.get('city'), formData.get('address'), formData.get('zip_code')]
                    .filter(Boolean).join(' ') || 'Not provided';
                document.getElementById('accountLocation').textContent = location;

                // Reload page to reflect changes
                location.reload();
            } else {
                showNotification('error', 'Error', data.error || 'Failed to update profile');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('error', 'Error', 'An error occurred while updating your profile');
        }
    });
}

// Handle Change Password Form Submission
const changePasswordForm = document.getElementById('changePasswordForm');
if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(changePasswordForm);
        const newPassword = formData.get('new_password');
        const confirmPassword = formData.get('confirm_password');

        // Validate passwords match
        if (newPassword !== confirmPassword) {
            showNotification('error', 'Error', 'New passwords do not match!');
            return;
        }

        try {
            const response = await fetch('/users/change-password/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification('success', 'Success', 'Password changed successfully!');
                changePasswordModal.style.display = 'none';
                changePasswordForm.reset();
            } else {
                showNotification('error', 'Error', data.error || 'Failed to change password');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('error', 'Error', 'An error occurred while changing your password');
        }
    });
}

// Handle Delete Account Form Submission
const deleteAccountForm = document.getElementById('deleteAccountForm');
if (deleteAccountForm) {
    deleteAccountForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(deleteAccountForm);

        // Final confirmation
        const confirmed = confirm('This action is PERMANENT and cannot be undone. Are you absolutely sure you want to delete your account?');
        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch('/users/delete-account/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification('success', 'Account Deleted', 'Your account has been deleted. You will now be redirected to the login page.');
                setTimeout(() => {
                    window.location.href = '/users/login/';
                }, 2000);
            } else {
                showNotification('error', 'Error', data.error || 'Failed to delete account. Please check your password.');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('error', 'Error', 'An error occurred while deleting your account');
        }
    });
}
