
$("#login_button").on("click", login);

function login()
{
    email = document.getElementById("email_login_field").value;
    password = document.getElementById("password_login_field").value;
    
    
    if(email.length > 1 && password.length > 1)
    {
    console.log(email, password);
    request_handler.sendLogin(email, password)
    }
    
}
