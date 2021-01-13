$(document).ready(function(){
    var details = document.getElementsByClassName('details');
    for(var i = 0;i < details.length; i++){
      details[i].setAttribute('title',details[i].innerHTML);
    }
});