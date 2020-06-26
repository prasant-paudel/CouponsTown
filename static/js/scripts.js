
    
    window.onscroll = function() {scrollFunction()};
    
    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scroll-navbar").style.top = "40px";
      } else {
        document.getElementById("scroll-navbar").style.top = "-200px";
      }
    }
