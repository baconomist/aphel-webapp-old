
var server_bridge = new ServerBridge();

function apply_error_to_input(input_element, error)
{
    remove_success_from_input(input_element);
    input_element.addClass("invalid_input");
    input_element.before("<span class='input_error'>" + error + "</span>")
}

function apply_success_to_input(input_element)
{
    remove_error_from_input(input_element);
    input_element.addClass("valid_input");
}

function remove_error_from_input(input_element)
{
    input_element.removeClass("invalid_input");
    input_element.parent().find(".input_error").remove();
}

function remove_success_from_input(input_element)
{
    input_element.removeClass("valid_input");
}



/*apply_error_to_input($("#signup_form").find("#email"));
apply_error_to_input($("#signup_form").find("#password"));
apply_error_to_input($("#signup_form").find("#password_confirm"));
apply_error_to_input($("#signup_form").find("#school"));*/
