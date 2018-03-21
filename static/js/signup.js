
$("#signup_button").on("click", signup);

function signup()
{
    email = document.getElementById("email_signup_field").value;
    password = document.getElementById("password_signup_field").value;
    
    
    if(email.length > 1 && password.length > 1)
    {
    console.log(email, password);
    request_handler.sendSignup(email, password)
    }
    
}
