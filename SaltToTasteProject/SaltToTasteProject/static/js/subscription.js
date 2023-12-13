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
        this.className = (data.status === 'subscribed') ? 'bnt-subscribe' : 'bnt-subscribe active'
        console.log(data.subs_count);
        document.getElementById('followers_count').textContent = data.subs_count;
//        console.log('Статус подписки:', data.status);
        // Обновите интерфейс в соответствии с новым статусом подписки
    })
    .catch(error => {
        console.error('Ошибка при обработке подписки:', error);
    });
});


const searchInput = document.getElementById('searchInput');
const cardContainer = document.querySelector('.users__card-container');

searchInput.addEventListener('input', () => {
    var userId = searchInput.getAttribute('data-profile-id');
    const searchQuery = (searchInput.value.charAt(0).toUpperCase() + searchInput.value.slice(1).toLowerCase()).trim();
    type = searchInput.getAttribute('data-type');

        fetch(`/account/profile/${userId}/${type}/search_${type}/?search=${searchQuery}`)
            .then(response => response.json())
            .then(data => {

            cardContainer.innerHTML = data.subs.map(sub => {
                const user = data.user;
                if (user.is_authenticated) {
                return `
                    <div class="users__card">
                        <div class="user__info">
                            <img class="rounded-circle account-img" src="/media/${sub.fields.avatar}">
                            <p class="card__username">@${sub.fields.username}</p>
                        </div>
                        <a class="bnt-subscribe ${sub.is_subscribed ? 'active' : ''}" data-profile-id="${sub.pk}" id="subscriptionBtn">${sub.is_subscribed ? 'Вы подписаны' : 'Подписаться'}</a>
                    </div>
                `;
                } else {
                    return `
                        <div class="users__card">
                            <div class="user__info">
                                <img class="rounded-circle account-img" src="/media/${sub.fields.avatar}">
                                <p class="card__username">@${sub.fields.username}</p>
                            </div>
                        </div>
                    `;
                }
            }

            ).join('');
        });
//    }
});