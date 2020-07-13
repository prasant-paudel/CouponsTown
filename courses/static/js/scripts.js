
    
    window.onscroll = function() {scrollFunction()};
    
    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scroll-navbar").style.top = "40px";
      } else {
        document.getElementById("scroll-navbar").style.top = "-200px";
      }
    }


window.onload = function(){
  document.getElementById("enroll-button")[0].disabled = true;
  setTimeout(function(){
    var element = discount.getElementById("enroll-button")[0];
    element.disabled = false;
  },5000);
}    