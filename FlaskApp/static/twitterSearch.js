function validateForm() {
    $('.alert').hide();
    var x = document.getElementById('inputText').value;
    $('.alert').hide();
    if (x == "") {
        $('.alert').show();
        return false;
    }
}

$('.timeline-Tweet').addEventListener("click", getTweet(this));

function getTweet(event) {
  var tweet = event.target;
  var val = tweet.querySelectorAll('.timeline-Tweet-text').innerText();
  console.log(val);
}
window.onload = function() {
  validateForm();

};
