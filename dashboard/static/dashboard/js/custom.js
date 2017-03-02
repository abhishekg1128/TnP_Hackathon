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
  if(pass.length<8){
    alert("Password should be at least 8 letters long!!");
    return false;
  }
  else if(pass!=reenter){
    alert("Passwords do not match!!");
    return false;
  }
}

function loadDoc(company_id)
{
  document.getElementById('student_detail').style.display = 'none';
    document.getElementById('company_detail').style.display = 'block';
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
     var data = JSON.parse(xhttp.responseText);
        document.getElementById('eligibility').innerHTML = 'Eligibilty : ' + data['eligibility'];
        document.getElementById('salary').innerHTML = 'Offered Salary : ' + data['salary'];
        document.getElementById('stipend').innerHTML = 'Offered Stipend(For Internship) : ' + data['stipend'];
        document.getElementById('last_date').innerHTML = 'LAST DATE OF REGISTRATION : ' + data['last_date'];

        if(data['can_apply'] == "true") {
            document.getElementById('apply_btn').className = 'btn btn-primary btn-default';
            document.getElementById('apply_btn').href = 'apply/' + company_id + "/";
        }
        else
          document.getElementById('apply_btn').className = 'btn btn-primary disabled';
    }
  };
  xhttp.open("GET", company_id, true);
  xhttp.send();
}