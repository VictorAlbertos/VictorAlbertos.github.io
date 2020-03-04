  $(document).on('show.bs.modal', '#submit-modal', function (e) {
    var tag = document.createElement("script");
    tag.src = "//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js";
    document.getElementsByTagName("head")[0].appendChild(tag);
  });

  function validate() {
  	$("#btn-submit").click(function(e) {
        setTimeout(function(){ location.reload();}, 2000);
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

  