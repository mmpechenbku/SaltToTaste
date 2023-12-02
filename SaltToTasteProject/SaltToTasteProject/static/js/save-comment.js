//Сохранение

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

//Сохранение рецепта
const saveButton = document.querySelectorAll('.save-recipe-button');

saveButton.forEach(button => {
    button.addEventListener('click', event => {
        const recipeId = parseInt(button.dataset.recipe)
        const saveSum = button.querySelector('.save-sum');
        const formData = new FormData();

        formData.append('recipe_id', recipeId);

        fetch("/search/save_recipe/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            if (data.status == 'created') {
                var save_status = '#fav_icon-enable';
            } else {
                var save_status = '#fav_icon';
            }
            button.innerHTML = '';
            button.innerHTML = '<svg width="32" height="32" class="navbar__item-search-img">' +
                                '<use href="' + save_status + '"></use>' +
                            '</svg>' +
                        '<span class="save-sum">' + data.save_sum + '</span>';
//            saveSum.textContent = data.save_sum;
        })
        .catch(error => console.error(error));
    });
});


// Комментарии рецептов

const commentForm = document.forms.commentForm;
const commentFormContent = commentForm.content;
const commentFormParentInput = commentForm.parent;
const commentFormSubmit = commentForm.commentSubmit;
const commentRecipeId = commentForm.getAttribute('data-recipe-id');

commentForm.addEventListener('submit', createComment);

replyUser()

function replyUser() {
    document.querySelectorAll('.btn-reply').forEach(e => {
        e.addEventListener('click', replyComment);
    });
}

function replyComment() {
    const commentUsername = this.getAttribute('data-comment-username');
    const commentMessageId = this.getAttribute('data-comment-id');

    commentFormContent.value = `${commentUsername}, `;
    console.log(commentFormParentInput.value);
    commentFormParentInput.value = commentMessageId;
    console.log(commentFormParentInput.value);
}
async function createComment(event) {
    event.preventDefault();
    commentFormSubmit.disabled = true;
    commentFormSubmit.innerText = "Ожидаем ответа сервера";
    try {
        const response = await fetch(`/search/recipe/${commentRecipeId}/comments/create/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new FormData(commentForm),
        });
        const comment = await response.json();

        var commentIndentation = '';
        if (comment.is_child) {
            commentIndentation = 'reply__comment';
        } else {
            commentIndentation = '';
        }

        //html для коммента
        let commentTemplate = `<ul id="comment-thread-${comment.id}">
        <li>
            <div class="comment__container ${commentIndentation}">
                <img src="${comment.avatar}" alt="${comment.author}">
                <div class="comment__content">
                    <div class="comment__header">
                        <p class="comment__nickname">${comment.author}</p>
                        <p class="comment__date">${comment.time_create}</p>
                    </div>
                    <div class="comment__text">
                        <p>${comment.content}</p>
                    </div>
                    <div class="comment__functions">
                        <svg width="24" height="24">
                            <a class="btn-reply" href="#commentForm" data-comment-id="${comment.id}"
                               data-comment-username="${comment.author}">
                                <use href="#reply"></use>
                            </a>
                        </svg>
                        <div class="like">
                            <svg width="18" height="18">
                                <use href="#like"></use>
                            </svg>
                            <p class="like-count">0</p>
                        </div>
                    </div>
                </div>
            </div>
        </li>
    </ul>`;

        if (comment.is_child) {
            console.log(comment.parent_id);
            document.querySelector(`#comment-thread-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
        }
        else {
            document.querySelector('.recipe__comments').insertAdjacentHTML("beforeend", commentTemplate)
        }
        commentForm.reset()
        commentFormSubmit.disabled = false;
        commentFormSubmit.innerText = "Добавить комментарий";
        commentFormParentInput.value = null;
        replyUser();
    }
    catch (error) {
        console.log(error)
    }
}


//лайк коммента
const likeButton = document.querySelectorAll('.like');

likeButton.forEach(button => {
    button.addEventListener('click', event => {
        const commentId = parseInt(button.dataset.comment);
        const likeSum = button.querySelector('.like-count');
        const formData = new FormData();

        formData.append('comment_id', commentId);

        fetch("/search/like_comment/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            button.innerHTML = '';
            let like_status = '#like';
            if (data.status == 'created') {
                like_status = '#like-enable';
            }
            if (data.status == 'deleted') {
                like_status = '#like';
            }
            button.innerHTML = '<svg width="18" height="18">' +
                                '<use href="' + like_status + '"></use>' +
                            '</svg>' +
                            '<p class="like-count">' + data.likes_sum + '</p>';
        })
        .catch(error => console.error(error));
    });
});
