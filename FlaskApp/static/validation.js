function validateForm() {
    $('.alert').hide();
    var x = document.getElementById('inputText').value;
    $('.alert').hide();
    if (x == "") {
        $('.alert').show();
        return false;
    }
}

window.onload = function() {
  validateForm();
};
