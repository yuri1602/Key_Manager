document.addEventListener("DOMContentLoaded", function () {
    const barcodeField = document.getElementById("barcode");
    const userSelect = document.getElementById("user_id");

    // Функция за автоматично фокусиране върху полето за баркод
    function focusBarcode() {
        if (document.activeElement !== userSelect) {
            barcodeField.focus();
        }
    }

    // Автоматично фокусиране при зареждане на страницата
    barcodeField.focus();

    // Събитие при промяна в падащото меню
    userSelect.addEventListener("change", function () {
        // Изчакване, за да се избегне моментално връщане на фокуса
        setTimeout(focusBarcode, 500);
    });

    // Фокусиране на полето за баркод при кликване извън други елементи
    document.addEventListener("click", function (event) {
        if (event.target !== userSelect && event.target !== barcodeField) {
            focusBarcode();
        }
    });
});
