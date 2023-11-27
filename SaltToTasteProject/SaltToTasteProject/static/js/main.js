/*Поиск по ингридиентам*/
const availableIngredientsContainer = document.querySelector('.available-ingredients');
const searchedIngredientsContainer = document.querySelector('.searched-ingredients');
const selectedIngredientsContainer = document.querySelector('.selected-ingredients');
const searchForm = document.getElementById('search-form');
const selectedIngredientIds = new Set();
const checkbox = document.getElementById('coincidence');

// Слушатель событий для доступных ингредиентов
availableIngredientsContainer.addEventListener('click', (event) => {
    const targetButton = event.target;
    if (targetButton.classList.contains('ingredient-button')) {
        const ingredientId = targetButton.getAttribute('data-ingredient-id');

        // Проверяем, является ли ингредиент уже выбранным
        if (!selectedIngredientIds.has(ingredientId)) {
            // Если ингредиент не выбран, добавляем его в выбранные
            selectedIngredientIds.add(ingredientId);

            // Создаем кнопку для выбранного ингредиента в поле "Выбранные ингредиенты"
            const selectedIngredientButton = document.createElement('button');
            selectedIngredientButton.type = 'button';
            selectedIngredientButton.className = 'ingredient-button selected';
            selectedIngredientButton.setAttribute('data-ingredient-id', ingredientId);
            selectedIngredientButton.textContent = targetButton.textContent;

            selectedIngredientsContainer.appendChild(selectedIngredientButton);
            ingredientSearchInput.value = '';
            ingredientButtonsContainer.innerHTML = '';
            checkbox.disabled = false;
        }

        // Запрещаем добавление этого ингредиента в "Доступные ингредиенты"
        targetButton.disabled = true;
        targetButton.style.display = 'none';
    }
});

// Слушатель событий для выбранных ингредиентов
selectedIngredientsContainer.addEventListener('click', (event) => {
    const targetButton = event.target;
    if (targetButton.classList.contains('ingredient-button')) {
        const ingredientId = targetButton.getAttribute('data-ingredient-id');

        // Удаляем ингредиент из выбранных
        selectedIngredientIds.delete(ingredientId);

        // Удаляем кнопку ингредиента из раздела "Выбранные ингредиенты"
        targetButton.remove();


        // Разрешаем добавление этого ингредиента в "Доступные ингредиенты"
        const correspondingAvailableButton = document.querySelector(`.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`);
        if (correspondingAvailableButton) {
            correspondingAvailableButton.disabled = false;
            correspondingAvailableButton.style.display = 'unset';

        }

        if (selectedIngredientIds.size == 0) {
            checkbox.checked = false;
            checkbox.disabled = true;
        }
    }
});

// Слушатель событий для отправки формы

searchForm.addEventListener('submit', (event) => {
    // Предотвращаем отправку формы при помощи обычного запроса
    event.preventDefault();

    // Собираем id выбранных ингредиентов
    const selectedIngredientIdsArray = Array.from(selectedIngredientIds);
    const selectedIngredientIdsString = selectedIngredientIdsArray.join(',');

    // Добавляем собранные id в скрытое поле формы
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'ingredients';
    hiddenInput.value = selectedIngredientIdsString;
    searchForm.appendChild(hiddenInput);

    // Отправляем форму на сервер
    searchForm.submit();
});

const ingredientSearchInput = document.getElementById('ingredient-search');
const ingredientButtonsContainer = document.getElementById('ingredient-buttons');


ingredientSearchInput.addEventListener('input', () => {
    const searchQuery = (ingredientSearchInput.value.charAt(0).toUpperCase() + ingredientSearchInput.value.slice(1).toLowerCase()).trim();

    // Очистить текущие кнопки ингредиентов
    ingredientButtonsContainer.innerHTML = '';

    if (searchQuery.length >= 2) {
        // Отправить AJAX запрос для получения ингредиентов по поисковому запросу
        fetch(`/search/api/ingredients/?search=${searchQuery}`)
            .then(response => response.json())
            .then(data => {
                // Создать кнопки для каждого найденного ингредиента
                data.forEach(ingredient => {
                    const button = document.createElement('button');
                    button.type = 'button';
                    button.className = 'ingredient-button';
                    button.setAttribute('data-ingredient-id', ingredient.id);
                    button.textContent = ingredient.name;
                    ingredientButtonsContainer.appendChild(button);

                    const ingredientId = button.getAttribute('data-ingredient-id');
                    if (selectedIngredientIds.has(ingredientId)) {
                        button.disabled = true;
                    }

                });
            });
    }
});
    ingredientButtonsContainer.addEventListener('click', (event) => {
        const targetButton = event.target;
        ingredientButtonsContainer.innerHTML = '';

        if (targetButton.classList.contains('ingredient-button')) {
            const ingredientId = targetButton.getAttribute('data-ingredient-id');

            // Проверяем, является ли ингредиент уже выбранным
            if (!selectedIngredientIds.has(ingredientId)) {
                // Если ингредиент не выбран, добавляем его в выбранные
                selectedIngredientIds.add(ingredientId);

                // Создаем кнопку для выбранного ингредиента в поле "Выбранные ингредиенты"
                const selectedIngredientButton = document.createElement('button');
                selectedIngredientButton.type = 'button';
                selectedIngredientButton.className = 'ingredient-button selected';
                selectedIngredientButton.setAttribute('data-ingredient-id', ingredientId);
                selectedIngredientButton.textContent = targetButton.textContent;

                selectedIngredientsContainer.appendChild(selectedIngredientButton);

                const correspondingAvailableButton = document.querySelector(`.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`);
                correspondingAvailableButton.disabled = true;
                ingredientSearchInput.value = '';

                checkbox.disabled = false;
            }

            // Запрещаем добавление этого ингредиента в "Доступные ингредиенты"
            targetButton.disabled = true;
        }
    });


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

const csrftoken = getCookie("csrftoken")

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
            saveSum.textContent = data.save_sum;
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
    commentFormContent.value = `${commnetUsername}, `;
    commentFormParentInput.value = commentMessageId;
}
async function createComment(event) {
    event.preventDefault();
    commentFormSubmit.disabled = true;
    commentFormSubmit.innerText = "Ожидаем ответа сервера";
    try {
        const response = await fetch(`/search/${commentRecipeId}/comments/create/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new FormData(commentForm),
        });
        const comment = await response.json();

        //html для коммента
        let commentTemplate = ``
        if (comment.is_child) {
            document.querySelector(`#comment-thread-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentTemplate);
        }
        else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate)
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

//const saveSelectionButton = document.querySelectorAll('.save');
//saveSelectionButton.forEach(button => {
//button.addEventListener('click', function () {

//const saveSelectionButton = document.querySelector('.save_selection');
//
//
//saveSelectionButton.addEventListener('click', function () {
//
//    var name = document.getElementById('collection-name').value;
//    var selectedRecipes = Array.from(document.querySelectorAll('input[name="recipes"]:checked')).map(checkbox => checkbox.value);
//
//    console.log(selectedRecipes);
//    console.log('lox');
//
//    var formData = new FormData();
//    formData.append('name', name);
//    selectedRecipes.forEach(recipeId => {
//        formData.append('recipes', recipeId);
//    });
//
//    // Отправляем POST-запрос
//    fetch('/search/create_selection/', {
//        method: 'POST',
//        body: formData,
//        credentials: 'same-origin',
//        headers: {
//                "X-CSRFToken": csrftoken,
//                "X-Requested-With": "XMLHttpRequest",
//        },
//    })
//    .then(response => response.json())
//    .then(data => {
//        console.log('Создана новая подборка:', data);
//        // Дополнительные действия после успешного создания подборки
//    })
//    .catch(error => {
//        console.error('Ошибка при создании подборки:', error);
//    });
//
//});
