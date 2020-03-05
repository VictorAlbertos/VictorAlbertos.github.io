document.addEventListener("DOMContentLoaded", function(){
  if (window.location.href.indexOf("welcome-message-subscribe") > -1) {
        var div = document.getElementById('subscribe-feedback');
        div.innerHTML = `
      <div class="alert alert-success bg-dark alert-dismissible" data-toggle="collapse">
        <a href="#" class="close " data-dismiss="alert" aria-label="close">&times;</a>
        <span class="text-white">¡Gracias por subscribirte a Desobra! Pronto recibirás nuestras actualizaciones.</span>
      </div>` + div.innerHTML;
    }
});

$(document).on('show.bs.modal', '#submit-modal', function (e) {
    var tag = document.createElement("script");
    tag.src = "//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js";
    document.getElementsByTagName("head")[0].appendChild(tag);
  });

  function validate() {
  	$("#btn-submit").click(function(e) {
        setTimeout(function(){ 
          window.location.search += '&welcome-message-subscribe=True';
        }, 500);
    });

    var valid = checkEmail($("#email"));
    
    $("#btn-submit").attr("disabled",true);
    if(valid) {
      $("#btn-submit").attr("disabled",false);
    } 
  }

  function checkEmpty(obj) {
    var name = $(obj).attr("name");
    $("."+name+"-validation").html(""); 
    if($(obj).val() == "") {
      return false;
    }
    
    return true;  
  }

  function checkEmail(obj) {
    var result = true;
    
    var name = $(obj).attr("name");
    $("."+name+"-validation").html(""); 
    
    result = checkEmpty(obj);
    
    if(!result) {
      return false;
    }
    
    var email_regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,3})+$/;
    result = email_regex.test($(obj).val());
    
    if(!result) {
      $("."+name+"-validation").html("Invalid");
      return false;
    }
    
    return result;  
  }

  