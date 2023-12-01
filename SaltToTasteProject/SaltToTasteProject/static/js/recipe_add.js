//обработка загрузки изображений
function inputSelected(count) {
  if (count) {
    var file = document.querySelector('#step-image-' + count).files[0];
    if (file) {
        document.querySelector('#file_add-' + count).setAttribute("href", "#accept_add");
        document.querySelector('#title_file-'+ count).textContent = "Изменить";
    } else {
        document.querySelector('#file_add-' + count).setAttribute("href", "#image_add");
        document.querySelector('#title_file-'+ count).textContent = "Добавить файл";
    }
  } else {
    var file = document.querySelector('#recipe_image').files[0];
    if (file) {
        document.querySelector('#file_add').setAttribute("href", "#accept_add");
        document.querySelector('#title_file').textContent = "Изменить";
    }
    else {
        document.querySelector('#file_add').setAttribute("href", "#image_add");
        document.querySelector('#title_file').textContent = "Добавить файл";
    }
  }
}

//добавление рецептов
        const availableIngredientsContainer = document.querySelector('.available-ingredients');
<!--        const selectedIngredientsContainer = document.querySelector('.selected-ingredients');-->
        const quantityIngredientsContainer = document.querySelector('.ingredient-quantity');
        const selectedIngredientIds = new Set();
        const recipeForm = document.getElementById('recipe-form');
        var ingredientCount = 0;
        var stepCount = 0;
        var maxSteps = 10;

        availableIngredientsContainer.addEventListener('click', (event) => {
            const targetButton = event.target;
            if (targetButton.classList.contains('ingredient-button')) {
                const ingredientId = targetButton.getAttribute('data-ingredient-id');

                if (!selectedIngredientIds.has(ingredientId)) {
                    var divSelectedContainer = document.createElement('div');
                    if ((ingredientCount % 2) == 0) {
                        divSelectedContainer.className = 'quantity__container gray';
                    }
                    else {
                        divSelectedContainer.className = 'quantity__container';
                    }
                    var divSelectedButtons = document.createElement('div');
                    divSelectedButtons.className = 'quantity__button';
                    selectedIngredientIds.add(ingredientId);
                    const selectedIngredientButton = document.createElement('button');
                    selectedIngredientButton.type = 'button';
                    selectedIngredientButton.className = 'ingredient-button selected';
                    selectedIngredientButton.setAttribute('data-ingredient-id', ingredientId);
                    selectedIngredientButton.setAttribute('name', 'quantity_button_' + ingredientId);
                    selectedIngredientButton.textContent = targetButton.textContent;

<!--                    selectedIngredientsContainer.appendChild(selectedIngredientButton);-->
                    quantityIngredientsContainer.appendChild(divSelectedContainer);
                    divSelectedContainer.appendChild(divSelectedButtons);
                    divSelectedButtons.appendChild(selectedIngredientButton);


                    var divQuantity = document.createElement('div');
                    divQuantity.className = 'quantity__input';
                    divQuantity.innerHTML = '<input data-quantity="' + selectedIngredientButton.getAttribute('data-ingredient-id') + '" name="quantity_' + selectedIngredientButton.getAttribute('data-ingredient-id') + '" placeholder="..."> <span class="selected-ingredients__delete" id="' + selectedIngredientButton.getAttribute('data-ingredient-id') + '">X</span>';
                    divSelectedContainer.appendChild(divQuantity);
                    ingredientCount++;
                }

                targetButton.disabled = true;
                targetButton.style.display = 'none';
            }
        });

        document.getElementById('add-step').addEventListener('click', function () {
            if (stepCount < maxSteps) {
                stepCount++;

                // Создадим новый div с полями для шага приготовления
                var stepsSection = document.getElementById('steps-section');
                var addedSteps = document.getElementById('added-steps');
                var div = document.createElement('div');
                div.className = 'ingredient__step-item';
                var currentStep = stepCount;
                div.innerHTML = '<div class="ingredient__step-item-img">' +
                                    '<label class="input-file-label" for="step-image-' + currentStep + '">' +
                                        '<svg width="64" height="64">' +
                                            '<use id="file_add-' + stepCount + '" href="#image_add"></use>' +
                                        '</svg>' +
                                        '<span id="title_file-' + stepCount + '">Добавить файл</span>' +
                                    '</label>' +
                                    '<input class="input-file" type="file" onchange="inputSelected(' + stepCount + ')" name="step_image_' + stepCount + '" accept=".png, .jpg, .jpeg" id="step-image-' + currentStep + '" required/>' +
                                '</div>' +
                                '<div class="ingredient__step-item-text">' +
                                    '<textarea name="step_description_' + stepCount + '" placeholder="Описание шага"  id="step-description-' + stepCount + '"></textarea>' +
                                '</div>' +
                                '<div class="ingredient__stepbnt-delete">' +
                                '<p>X</p>' +
                                '</div>';


                // Добавляем созданный div в разметку
                addedSteps.appendChild(div);

                // Проверяем, нужно ли скрыть кнопку "Добавить шаг"
                if (stepCount === maxSteps) {
                    document.getElementById('add-step').style.display = 'none';
                }
            }
            document.getElementById('step-description-' + currentStep).addEventListener('input', function () {
                // Обновляем краткое описание
                updateSummary();
            });
        });

         function updateSummary() {
            var summaryList = document.getElementById('summary-list');
            summaryList.innerHTML = ''; // Очищаем текущий список

            // Проходим по всем добавленным шагам и добавляем их в список
            for (var i = 0; i < stepCount; i++) {
                var stepDescription = document.getElementById('step-description-' + (i + 1)).value;

                var listItem = document.createElement('li');
                listItem.textContent = stepDescription;

                summaryList.appendChild(listItem);
            }
         }

         quantityIngredientsContainer.addEventListener('click', (event) => {
             const targetButton = event.target;
             if (targetButton.classList.contains('selected-ingredients__delete')) {
                 const ingredientId = targetButton.getAttribute('id');

                 var quantityField = document.querySelector('[name="quantity_' + ingredientId + '"]');
                 quantityField.remove();
                 // Удаляем ингредиент из выбранных
                 selectedIngredientIds.delete(ingredientId);

                 // Удаляем кнопку ингредиента из раздела "Выбранные ингредиенты"
                 var quantitySelectedButton = document.querySelector('[name="quantity_button_' + ingredientId + '"]');
                 quantitySelectedButton.remove();
                 targetButton.remove();
                  ingredientCount--;


                 // Разрешаем добавление этого ингредиента в "Доступные ингредиенты"
                 const correspondingAvailableButton = document.querySelector(`.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`);
                 if (correspondingAvailableButton) {
                     correspondingAvailableButton.disabled = false;
                     correspondingAvailableButton.style.display = 'unset';

                 }

             }
         });

        document.getElementById('save-recipe').addEventListener('click', function () {

            const selectedIngredientIdsArray = Array.from(selectedIngredientIds);
            const selectedIngredientIdsString = selectedIngredientIdsArray.join(',');

            // Добавляем собранные id в скрытое поле формы
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'ingredients';
            hiddenInput.value = selectedIngredientIdsString;
            recipeForm.appendChild(hiddenInput);

            // Собираем данные формы
            var formData = new FormData(document.getElementById('recipe-form'));

            // Добавляем данные о количестве ингредиентов
            formData.append('ingredients_count', ingredientCount);

            // Добавляем данные о количестве шагов
            formData.append('steps_count', stepCount);

            // Отправляем данные на сервер
            fetch('/search/recipe_add/', {
              method: 'POST',
              body: formData
            })
            .then(response => response.json())
            .then(data => {
              if (data.status === 'success') {
                alert('Рецепт успешно сохранен!');
                window.location.href = "{% url 'search' %}";
                // Дополнительные действия после успешного сохранения
              } else {
                alert('Произошла ошибка при сохранении рецепта.');
                console.log(data.message);
              }
            })
            .catch(error => {
              console.error('Ошибка при отправке данных на сервер:', error);
            });
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
                    var divSelectedContainer = document.createElement('div');
                    if ((ingredientCount % 2) == 0) {
                        divSelectedContainer.className = 'quantity__container gray';
                    }
                    else {
                        divSelectedContainer.className = 'quantity__container';
                    }
                    var divSelectedButtons = document.createElement('div');
                    divSelectedButtons.className = 'quantity__button';
                // Если ингредиент не выбран, добавляем его в выбранные
                selectedIngredientIds.add(ingredientId);

                // Создаем кнопку для выбранного ингредиента в поле "Выбранные ингредиенты"
                const selectedIngredientButton = document.createElement('button');
                selectedIngredientButton.type = 'button';
                selectedIngredientButton.className = 'ingredient-button selected';
                selectedIngredientButton.setAttribute('data-ingredient-id', ingredientId);
                selectedIngredientButton.setAttribute('name', 'quantity_button_' + ingredientId);
                selectedIngredientButton.textContent = targetButton.textContent;

                quantityIngredientsContainer.appendChild(divSelectedContainer);
                divSelectedContainer.appendChild(divSelectedButtons);
                divSelectedButtons.appendChild(selectedIngredientButton);


                    var divQuantity = document.createElement('div');
                    divQuantity.className = 'quantity__input';
                    divQuantity.innerHTML = '<input data-quantity="' + selectedIngredientButton.getAttribute('data-ingredient-id') + '" name="quantity_' + selectedIngredientButton.getAttribute('data-ingredient-id') + '" placeholder="..."> <span class="selected-ingredients__delete" id="' + selectedIngredientButton.getAttribute('data-ingredient-id') + '">X</span>';
                    divSelectedContainer.appendChild(divQuantity);
                    ingredientCount++;

                const correspondingAvailableButton = document.querySelector(`.available-ingredients .ingredient-button[data-ingredient-id="${ingredientId}"]`);
                correspondingAvailableButton.disabled = true;
                ingredientSearchInput.value = '';
                checkbox.disabled = false;
            }

            // Запрещаем добавление этого ингредиента в "Доступные ингредиенты"
            targetButton.disabled = true;
        }
    });


