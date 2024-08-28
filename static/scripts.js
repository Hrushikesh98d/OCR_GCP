document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('input[type="submit"]');
    submitButton.addEventListener('click', function() {
        submitButton.value = 'Processing...';
        submitButton.disabled = true;
    });
});
