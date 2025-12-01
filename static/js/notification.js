document.addEventListener('DOMContentLoaded', function () {
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const notificationList = document.getElementById('notificationList');
    const notificationCount = document.getElementById('notificationCount');

    const openNotificationsBtnMobile = document.getElementById('openNotificationsBtnMobile');
    const closeNotificationDropdown = document.getElementById('closeNotificationDropdown');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // Toggle dropdown (Desktop)
    if (notificationBtn) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.toggle('show');
        });
    }

    // Open dropdown (Mobile Sidebar)
    if (openNotificationsBtnMobile) {
        openNotificationsBtnMobile.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.add('show');
            // Close sidebar
            if (sidebar) sidebar.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
        });
    }

    // Close dropdown (Mobile Close Button)
    if (closeNotificationDropdown) {
        closeNotificationDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.remove('show');
        });
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (notificationDropdown && notificationDropdown.classList.contains('show')) {
            // On mobile, clicking outside (on the backdrop if any, or just body) should close it
            // But we need to be careful not to close it immediately if we just opened it
            if (!notificationDropdown.contains(e.target) &&
                (!notificationBtn || !notificationBtn.contains(e.target)) &&
                (!openNotificationsBtnMobile || !openNotificationsBtnMobile.contains(e.target))) {
                notificationDropdown.classList.remove('show');
            }
        }
    });

    // Fetch notifications
    fetchNotifications();

    function fetchNotifications() {
        fetch('/api/notifications/')
            .then(response => response.json())
            .then(data => {
                renderNotifications(data.notifications);
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }

    function renderNotifications(notifications) {
        if (!notifications || notifications.length === 0) {
            notificationList.innerHTML = '<p class="empty-message">No new notifications.</p>';
            notificationCount.textContent = '0';
            notificationCount.style.display = 'none';
            return;
        }

        const unreadCount = notifications.filter(n => !n.is_read).length;
        notificationCount.textContent = unreadCount;
        notificationCount.style.display = unreadCount > 0 ? 'block' : 'none';

        notificationList.innerHTML = notifications.map(notification => `
            <div class="notification-item ${notification.is_read ? 'read' : 'unread'}" data-id="${notification.id}">
                <div class="notification-icon">
                    <i class="fas fa-ticket-alt"></i>
                </div>
                <div class="notification-content">
                    <p class="notification-message">${notification.message}</p>
                    <span class="notification-time">${notification.created_at}</span>
                </div>
                ${!notification.is_read ? `
                <button class="mark-read-btn" onclick="markAsRead(${notification.id}, event)" title="Mark as read">
                    <i class="fas fa-check"></i>
                </button>
                ` : ''}
            </div>
        `).join('');
    }

    // Make markAsRead globally available
    window.markAsRead = function (id, event) {
        if (event) event.stopPropagation();

        fetch(`/api/notifications/mark-read/${id}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Refresh notifications
                    fetchNotifications();
                }
            })
            .catch(error => console.error('Error marking notification as read:', error));
    };
});
