// ------------------------------------------------------------------
// maths.js
// Funciones de JavaScript
// realiza las operaciones de suma, resta, multiplicación y división
// ------------------------------------------------------------------

$(function() {
    // Verifica que se haya dado click en el botón identificado como calc
    $('#calc').click(function() {
        // Ejecuta AJAX
        $.ajax({
            // Define la url en la que se ejecutará
            url: '/api/calc?a=' + document.getElementById('a').value +
                '&b=' + document.getElementById('b').value +
                '&c=' + document.getElementById('c').value,
            // La función success
            success: function(data) {
                // Coloca los datos en los DIV
                $('#add').html(data['agua'] + ' + ' + data['pan'] + ' = ' + data['resSuma']);
                $('#subtract').html(data['agua'] + ' - ' + data['pan'] + ' = ' + data['resRest']);
                $('#multiply').html(data['agua'] + ' * ' + data['pan'] + ' = ' + data['resMult']);
                $('#divide').html(data['agua'] + ' / ' + data['pan'] + ' = ' + data['resDivi']);
                $('#csv').html(data['agua'] + ' / ' + data['pan'] + ' = ' + data['lc']);
            }
        });
    });
})