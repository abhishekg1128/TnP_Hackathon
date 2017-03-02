$(document).ready(function(){


  $(".submenu > a").click(function(e) {
    e.preventDefault();
    var $li = $(this).parent("li");
    var $ul = $(this).next("ul");

    if($li.hasClass("open")) {
      $ul.slideUp(350);
      $li.removeClass("open");
    } else {
      $(".nav > li > ul").slideUp(350);
      $(".nav > li").removeClass("open");
      $ul.slideDown(350);
      $li.addClass("open");
    }
  });

});

function validateForm()
{
  var pass =  document.getElementById('pass').value;
  var reenter = document.getElementById('reenter_pass').value;
  if(pass.length<6){
    alert("Password should be atleast 6 letters long!!");
    return false;
  }
  else if(pass!=reenter){
    alert("Passwords do not match!!");
    return false;
  }
}
