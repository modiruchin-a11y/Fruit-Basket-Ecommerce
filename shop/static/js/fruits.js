document.querySelectorAll('.toggle-btn').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();

        const parent = this.parentElement;
        const shortText = parent.querySelector('.short-text');
        const fullText = parent.querySelector('.full-text');

        // Check if elements exist to prevent errors
        if (!shortText || !fullText) return;

        if (fullText.classList.contains('d-none')) {
            // Full text dikhao aur short text chhupao
            fullText.classList.remove('d-none');
            shortText.classList.add('d-none');
            this.textContent = 'Show Less';
        } else {
            // Short text dikhao aur full text chhupao
            fullText.classList.add('d-none');
            shortText.classList.remove('d-none');
            this.textContent = 'Show More';
        }
    });
});