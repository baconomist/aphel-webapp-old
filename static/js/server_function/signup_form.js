// Stop button redirect,
// return false so its as if button was not clicked
/*$("#signup_button").on("click", function(){
    if()
    return false;
});*/

function run_password_error_check()
{
    var password = $("#signup_form").find("#password").val();
    var password_confirm = $("#signup_form").find("#password_confirm").val();
    
    console.log(password.toString().length);
    
    if(password.toString().length < 8)
    {
        apply_error_to_input($("#signup_form").find("#password"), "Password should be at least 8 characters long.");
    }
    else if(password == password_confirm)
    {
        apply_success_to_input($("#signup_form").find("#password"));
        apply_success_to_input($("#signup_form").find("#password_confirm"));
    } 
    else if(password_confirm.toString().length > 0)
    {
        apply_error_to_input($("#signup_form").find("#password"), "Passwords do not match!")   
        apply_error_to_input($("#signup_form").find("#password_confirm"), "Passwords do not match!")    
    }    
    else
    {
        apply_success_to_input($("#signup_form").find("#password"));
    }
}

function run_email_error_check()
{
    var email = $("#signup_form").find("#email").val();
    
    if(!email.includes("@pdsb.net"))
    {
        apply_error_to_input($("#signup_form").find("#email"), "Please user your @pdsb.net email!");
    }
    else{
        server_bridge.sendToServer("/", data={"function":"user_exists", "data":email}, function(response){

            if(response["data"])
            {
                apply_error_to_input($("#signup_form").find("#email"), "Username already exists!");
            }   
            else
            {
                apply_success_to_input($("#signup_form").find("#email"));
            }
        });  
    }
    
}

// When user leaves the email box
$("#signup_form").find("#email").on("blur", function(){
    
    run_email_error_check(); 
    
});

$("#signup_form").find("#password").on("blur", function(){
    
    run_password_error_check();
    
    var password = $("signup_form").find("#password").val();
    
    server_bridge.sendToServer("/", data={"function":"is_password_valid", "data":password}, function(response){
        
        if(response["data"])
        {
            
        }
        else
        {
                
        }
        
    });
    
});

$("#signup_form").find("#password_confirm").on("blur", function(){
    run_password_error_check();    
});

$("#signup_form").on("submit", function(){
    
    console.log("Signing up...");
    
    // get all the inputs into an array.
    var inputs = $('#signup_form :input');
    
    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    inputs.each(function() {
        values[this.id] = $(this).val();
    });
    
    console.log("Password: " + values["password"] + " Email: " + values["email"]);
    
    //if(values["password"].length >= 8 && values["password"] == values["password_confirm"]){
    console.log("Signing up!");
    server_bridge.sendToServer("/signup", values, function(response){
        console.log(response["data"]);
    });
    //}
    
    // Don't post to server/refresh the page
    return false;
    
});
  