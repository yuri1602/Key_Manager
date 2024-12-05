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
    focusBarcode();

    // Автоматично фокусиране, когато не сме в падащото меню
    document.addEventListener("click", function (event) {
        if (event.target !== userSelect) {
            focusBarcode();
        }
    });
});
