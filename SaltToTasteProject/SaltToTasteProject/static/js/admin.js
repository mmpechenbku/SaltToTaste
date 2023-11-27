document.addEventListener('DOMContentLoaded', function () {

    // Получаем ссылки на элементы select и tbody
    var ingredientSelect = document.getElementById('id_ingredients');
    var quantityTBody = document.getElementById('ingredientquantity_set-group').querySelector('tbody');
    var addRow = quantityTBody.querySelector('.add-row');

    // Счетчик добавленных ингредиентов
    var ingredientCounter = 0;

    console.log(ingredientCounter);
//    // Скрываем изначально tbody
//    if (ingredientCounter == 0) {
//        quantityTBody.style.display = 'none';
//        console.log('there');
//    };

    // Добавляем обработчик события изменения выбора в ингредиенте
    ingredientSelect.addEventListener('change', function () {
        // Получаем выбранные ингредиенты
        var selectedIngredients = [];
        for (var i = 0; i < ingredientSelect.options.length; i++) {
            if (ingredientSelect.options[i].selected) {
                selectedIngredients.push({
                    value: ingredientSelect.options[i].value,
                    text: ingredientSelect.options[i].text
                });
            }
        }

        // Если выбран хотя бы один ингредиент, отображаем tbody
        if (selectedIngredients.length > 0) {
            quantityTBody.style.display = 'table-row-group';
        } else {
            quantityTBody.style.display = 'none';
        }

        // Очищаем все текущие строки в tbody
        while (quantityTBody.firstChild) {
            quantityTBody.removeChild(quantityTBody.firstChild);
        }

        // Создаем строки для каждого выбранного ингредиента
        for (var j = 0; j < selectedIngredients.length; j++) {
            addIngredientRow(selectedIngredients[j].value, selectedIngredients[j].text);
        }
    });


    function addIngredientRow(ingredientValue, ingredientText) {
        // Создаем новую строку
        var newRow = quantityTBody.insertRow();

        var originalTd = newRow.insertCell(0);
        var origTd = document.createElement('td');
        origTd.className = 'original';
        originalTd.appendChild(origTd);

        // Создаем ячейку для ингредиента и добавляем select
        var cellIngredient = newRow.insertCell(1);
        var ingredientSelectCell = document.createElement('select');
        ingredientSelectCell.name = 'ingredientquantity_set-' + ingredientCounter + '-ingredient';
        ingredientSelectCell.id = 'id_ingredientquantity_set-' + ingredientCounter + '-ingredient';

        // Копируем все опции из основного select
        for (var k = 0; k < ingredientSelect.options.length; k++) {
                var option = document.createElement('option');
                option.value = ingredientSelect.options[k].value;
                option.text = ingredientSelect.options[k].text;
                if (ingredientSelect.options[k].selected){
                    option.disabled = true;
                }
                ingredientSelectCell.add(option);
        }

        ingredientSelectCell.addEventListener('change', function() {
            ingredientValue = ingredientSelectCell.value;
            var ingredientSelects = document.querySelectorAll('[id^="id_ingredientquantity_set-"][id$="-ingredient"]');
            var selected = [];
            ingredientSelects.forEach(function (select){
                for (var k = 0; k < ingredientSelect.options.length; k++) {
                   if (select.options[k].selected) {
                        selected.push(select.options[k])
                    }
                }
            })
            for (var k = 0; k < ingredientSelect.options.length; k++) {
                ingredientSelect.options[k].selected = false;
            }

            for (var k = 0; k < ingredientSelect.options.length; k++) {
                for (var j = 0; j < selected.length; j++) {
                    if (ingredientSelect.options[k].value == selected[j].value){
                        ingredientSelect.options[k].selected = true;
                        break;
                    }
                }
            }
            ingredientSelects.forEach(function (select) {
                for (var k = 0; k < ingredientSelect.options.length; k++) {
                    if (ingredientSelect.options[k].selected) {
                        select.options[k].disabled = true;
                    } else {
                        select.options[k].disabled = false;
                    }
                }
            })
        });

        // Выбираем добавленный ингредиент
        ingredientSelectCell.value = ingredientValue;

        // Добавляем select в ячейку
        cellIngredient.appendChild(ingredientSelectCell);

        // Создаем ячейку для ссылки изменения ингредиента
        var changeLink = createLink('change', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(changeLink);

        // Создаем ячейку для ссылки добавления нового ингредиента
        var addLink = createLink('add', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(addLink);

        // Создаем ячейку для ссылки просмотра
        var viewLink = createLink('view', ingredientCounter, ingredientValue);
        cellIngredient.appendChild(viewLink);

        ingredientSelectCell.addEventListener('change', function() {
            changeLink.href = '/admin/recipes/ingredient/' + ingredientSelectCell.value + '/change/?_to_field=id&_popup=1';
            viewLink.href = '/admin/recipes/ingredient/' + ingredientSelectCell.value + '/change/?_to_field=id';
        });

        // Создаем ячейку для количества и добавляем поле ввода
        var cellQuantity = newRow.insertCell(2);
        var quantityInput = document.createElement('input');
        quantityInput.type = 'text';
        quantityInput.name = 'ingredientquantity_set-' + ingredientCounter + '-quantity';
        quantityInput.id = 'id_ingredientquantity_set-' + ingredientCounter + '-quantity';
        quantityInput.className = 'vTextField';
        cellQuantity.appendChild(quantityInput);

        // Создаем ячейку для ссылки удаления
        var cellDelete = newRow.insertCell(3);
        var deleteLink = document.createElement('a');
        deleteLink.textContent = 'Удалить';
        deleteLink.className = 'inline-deletelink';
        deleteLink.href = '#';  // добавляем атрибут href для предотвращения перехода по ссылке
        deleteLink.addEventListener('click', function (event) {

            var ingredientSelects = document.querySelectorAll('[id^="id_ingredientquantity_set-"][id$="-ingredient"]');

            event.preventDefault();  // предотвращаем переход по ссылке

            // Удаляем строку
            quantityTBody.removeChild(newRow);
//             Снимаем выбор ингредиента из основного select
            for (var i = 0; i < ingredientSelect.options.length; i++) {
                if (ingredientSelect.options[i].value === ingredientValue) {
                    console.log(ingredientValue);
                    ingredientSelect.options[i].selected = false;
                    ingredientSelects.forEach(function (select) {
                        select.options[i].disabled = false;
                    });
                    break;
                }
            }
        });
        cellDelete.appendChild(deleteLink);

        // Увеличиваем счетчик добавленных ингредиентов
        ingredientCounter++;
    }

    function createLink(type, counter, ingredientValue) {
        var link = document.createElement('a');
        link.className = 'related-widget-wrapper-link ' + type + '-related';
        link.id = type + '_id_ingredientquantity_set-' + counter + '-ingredient';
        link.href = '/admin/recipes/ingredient/' + ingredientValue + '/' + type + '/?_to_field=id&_popup=1';
        link.title = getTitle(type);
        link.setAttribute('data-popup', 'yes');  // Добавляем атрибут для открытия в popup
        var img = document.createElement('img');
        img.src = '/static/admin/img/icon-' + type + 'link.svg';
        img.alt = getTitle(type);
        link.appendChild(img);
        return link;
    }

    function getTitle(type) {
        switch (type) {
            case 'change':
                return 'Изменить выбранный объект типа "Ингредиент"';
            case 'add':
                return 'Добавить ещё один объект типа "Ингредиент"';
            case 'view':
                return 'Просмотреть выбранный объект типа "Ингредиент"';
            default:
                return '';
        }
    }

});

//document.addEventListener('DOMContentLoaded', function () {
//    var stepsContainer = document.getElementById('steps-group');
//    console.log(stepsContainer);
//    var addStepButton = stepsContainer.querySelector('.add-row');
//    console.log(addStepButton);
//
//    addStepButton.addEventListener('click', function () {
//        // Находим все инпуты с номерами шагов
//        var stepNumberInputs = stepsContainer.querySelectorAll('[name^="steps-"][name$="-step_number"]');
//
//        // Вычисляем максимальный номер шага
//        var maxStepNumber = 0;
//        stepNumberInputs.forEach(function (input) {
//            var stepNumber = parseInt(input.value, 10);
//            if (!isNaN(stepNumber) && stepNumber > maxStepNumber) {
//                maxStepNumber = stepNumber;
//            }
//        });
//
//        // Увеличиваем максимальный номер шага на 1
//        var newStepNumber = maxStepNumber + 1;
//
//        // Находим поля для нового шага
//        var newStepFields = stepsContainer.querySelector('[id^="steps-empty"]').cloneNode(true);
//
//        // Заменяем placeholder внутри клонированных полей
//        newStepFields.innerHTML = newStepFields.innerHTML.replace(/__prefix__/g, newStepNumber);
//
//        // Вставляем новые поля в конец контейнера шагов
//        stepsContainer.insertBefore(newStepFields, addStepButton.parentNode);
//    });
//});