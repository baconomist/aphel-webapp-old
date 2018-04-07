
var server_bridge = new ServerBridge();

function apply_error_to_input(input_element, error)
{
    try
    {
        remove_success_from_input(input_element);
    }
    catch(err){}
    
    try
    {
        remove_error_from_input(input_element);
    }
    catch(err){
        console.log(err);
    }
    
    
    
    input_element.addClass("invalid_input");
    input_element.before("<span class='input_error' id=" + input_element.attr("id") + "_error >" + error + "</span>")
}

function apply_success_to_input(input_element)
{
    try
    {
    remove_error_from_input(input_element);
    }
    catch(err){}
    input_element.addClass("valid_input");
}

function remove_error_from_input(input_element)
{
    input_element.removeClass("invalid_input");
    console.log(input_element.attr("id"));
    input_element.parent().find("#" + input_element.attr("id") + "_error").remove();
}

function remove_success_from_input(input_element)
{
    input_element.removeClass("valid_input");
}



/*apply_error_to_input($("#signup_form").find("#email"));
apply_error_to_input($("#signup_form").find("#password"));
apply_error_to_input($("#signup_form").find("#password_confirm"));
apply_error_to_input($("#signup_form").find("#school"));*/
