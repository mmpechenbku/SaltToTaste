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


//var subscriptionBtn = document.getElementById('subscriptionBtn');
//
//subscriptionBtn.addEventListener('click', function() {

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
//        document.getElementById('subscriptionBtn')
        this.textContent = (data.status === 'subscribed') ? 'Вы подписаны' : 'Подписаться';
        console.log(data.subs_count);
        document.getElementById('followers_count').textContent = data.subs_count;
//        console.log('Статус подписки:', data.status);
        // Обновите интерфейс в соответствии с новым статусом подписки
    })
    .catch(error => {
        console.error('Ошибка при обработке подписки:', error);
    });
});