// Funções JavaScript globais podem ser adicionadas aqui
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Formatação de campos numéricos
    document.querySelectorAll('.currency-input').forEach(function(element) {
        new Cleave(element, {
            numeral: true,
            numeralThousandsGroupStyle: 'thousand',
            numeralDecimalMark: ',',
            delimiter: '.',
            prefix: 'R$ '
        });
    });
});