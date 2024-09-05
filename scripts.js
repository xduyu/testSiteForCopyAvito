document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/announcements')
        .then(response => response.json())
        .then(data => {
            const announcementsList = document.getElementById('announcements-list');
            if (!announcementsList) {
                console.error('Element with id "announcements-list" not found');
                return;
            }

            announcementsList.innerHTML = '';

            if (data.length === 0) {
                announcementsList.innerHTML = '<p>No announcements found.</p>';
                return;
            }

            data.forEach(announcement => {
                const announcementElement = document.createElement('div');
                announcementElement.className = 'announcement';
                announcementElement.innerHTML = `
                    <h2><a href="announcement.html?id=${announcement.id}">${announcement.title}</a></h2>
                    <p>${announcement.content}</p>
                    <p><strong>Name:</strong> ${announcement.name || 'Not provided'}</p>
                    <p><strong>Contact:</strong> ${announcement.contact || 'Not provided'}</p>
                    ${announcement.image ? `<img src="${announcement.image}" alt="Image" style="max-width 100%;max-height: 250px;">` : ''}
                `;
                announcementsList.appendChild(announcementElement);
            });
        })
        .catch(error => {
            console.error('Error fetching announcements:', error);
        });

    const form = document.getElementById('announcement-form');
    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();

            const title = document.getElementById('title').value;
            const content = document.getElementById('content').value;
            const name = document.getElementById('name').value;
            const contact = document.getElementById('contact').value;
            const image = document.getElementById('image').files[0]; // Изображение

            const formData = new FormData();
            formData.append('title', title);
            formData.append('content', content);
            formData.append('name', name);
            formData.append('contact', contact);
            if (image) formData.append('image', image);

            try {
                const response = await fetch('http://127.0.0.1:5000/announcements', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    window.location.href = 'index.html'; // Перенаправление обратно на главную страницу
                } else {
                    const errorData = await response.json();
                    console.error('Error adding announcement:', errorData);
                    alert(`Error adding announcement: ${errorData.error || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while adding the announcement.');
            }
        });
    }
});
