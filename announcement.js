document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');

    if (id) {
        fetch(`http://127.0.0.1:5000/announcements/${id}`)
            .then(response => response.json())
            .then(data => {
                const detailDiv = document.getElementById('announcement-detail');
                
                detailDiv.innerHTML = `
                    <h2>${data.title}</h2>
                    ${data.image ? `<img src="${data.image}" alt="Image">` : ''}
                    <p>${data.content}</p>
                    <div class="contact-info">
                        <h3>Контактная информация</h3>
                        <p><strong>Имя:</strong> ${data.name || 'Не указано'}</p>
                        <p><strong>Контакт:</strong> ${data.contact || 'Не указан'}</p>
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error fetching announcement details:', error);
            });
    } else {
        document.getElementById('announcement-detail').innerHTML = '<p>Объявление не найдено.</p>';
    }
});
