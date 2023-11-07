let btnSign = document.querySelector(".shine-button_signin");

btnSign.onclick = () => {
    let popupUp = document.querySelector(".signup__popup");
	let popupIn = document.querySelector(".signin__popup");
	let btnSignin = document.querySelector(".btn__signin");
	let popup = document.querySelector(".sign__container");
	popup.classList.add("sign__container_active");
    popupIn.classList.add("signin__popup_active");
    btnSignin.classList.add("btn__signin_active");

	let btnSignup = document.querySelector(".btn__signup");
	btnSignup.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.add("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.add("btn__signup_active");
	}
/*	let btnSignin = document.querySelector(".btn__signin");*/
	btnSignin.onclick = () => {
	popupUp.classList.remove("signup__popup_active");
	popupIn.classList.add("signin__popup_active");
	btnSignup.classList.remove("btn__signup_active");
	btnSignin.classList.add("btn__signin_active");
	}
	let btnExit = document.querySelector(".sign_background");
	let btnX = document.querySelector(".cl-btn-7");
	btnX.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.remove("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.remove("btn__signup_active");
 	popup.classList.remove("sign__container_active");
 }
	btnExit.onclick = () => {
	popupIn.classList.remove("signin__popup_active");
    popupUp.classList.remove("signup__popup_active");
    btnSignin.classList.remove("btn__signin_active");
    btnSignup.classList.remove("btn__signup_active");
 	popup.classList.remove("sign__container_active");
 }
}
/*---------------------------------------------------------------*/

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



