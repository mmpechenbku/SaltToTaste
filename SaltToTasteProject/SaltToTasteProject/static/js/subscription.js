const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

const csrftoken = getCookie("csrftoken");

document.getElementById('subscriptionBtn').addEventListener('click', function() {
    var userId = this.getAttribute('data-profile-id');

    fetch('/account/subscription/' + userId + '/', {
        method: 'POST',
        headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
        },
//        credentials: 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Статус подписки:', data.status);
        // Обновите интерфейс в соответствии с новым статусом подписки
    })
    .catch(error => {
        console.error('Ошибка при обработке подписки:', error);
    });
});