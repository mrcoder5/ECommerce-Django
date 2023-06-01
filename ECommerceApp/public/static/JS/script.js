var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  
  return new bootstrap.Toast(toastEl, option)
});

 
$(document).ready(function() {
  $('.carousel').carousel({
    interval: 4000,
    wrap: true
  });
});
