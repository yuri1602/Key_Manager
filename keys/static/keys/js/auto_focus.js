document.addEventListener('DOMContentLoaded', function() {
    // Изберете първото текстово поле на страницата
    const firstInputField = document.querySelector('input[type="text"]');
    if (firstInputField) {
        firstInputField.focus();

        // Ако фокусът се загуби, го възстановете
        firstInputField.addEventListener('blur', function() {
            setTimeout(() => firstInputField.focus(), 100);
        });
    }
});
