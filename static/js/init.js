
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
    input_element.parent().find("#" + input_element.attr("id") + "_error").remove();
}

function remove_success_from_input(input_element)
{
    input_element.removeClass("valid_input");
}

function recursive_id_change(element, change)
{
    element.children().each(function () {
        if(this.id.length > 0)
        {
            this.id = this.id + change;
            console.log(this.id);
        }
        jQueryElement = $(this);
        recursive_id_change(jQueryElement, change);
    });
}

function is_user_logged_in(callback)
{
    if(JSON.parse(getCookie("login")) != null){
        
        server_bridge.sendToServer("/", {"function": "login", "data": {"login": JSON.parse(getCookie("login"))} }, function(response){
            if(response["data"])
            {
                console.log("**login_check** Logged in.");
                callback(true);
            }
            else
            {
                console.log("**login_check** Not logged in.");
                callback(false);
            }
        });
    }
    else
    {
        console.log("**login_check** Not logged in.");
        callback(false);    
    }
}

function login_check()
{
    if(JSON.parse(getCookie("login")) != null){
        server_bridge.sendToServer("/", {"function": "login", "data": {"login": JSON.parse(getCookie("login"))} }, function(response){
            if(response["data"])
            {
                console.log("**login_check** Logged in.");
            }
            else
            {
                console.log("**login_check** Not logged in!");

                $('body').append('<div role="dialog" tabindex="-1" class="modal fade" id="failed_login_modal"><div class="modal-dialog modal-dialog-centered" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button></div><div class="modal-body"><p>Failed to log in. Please make sure you have the correct login information.</p></div><div class="modal-footer"><button class="btn btn-primary" type="button" id="close_modal_button">Close</button></div></div></div></div>'); 
                $('body').find("#failed_login_modal").modal('show');   

                $('body').find("#failed_login_modal").find("#close_modal_button").on('click', function(){
                    $('body').find("#failed_login_modal").modal("hide");
                });

            }
        });   
    }
    else
    {
        console.log("**login_check** Not logged in!");

        $('body').append('<div role="dialog" tabindex="-1" class="modal fade" id="failed_login_modal"><div class="modal-dialog modal-dialog-centered" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button></div><div class="modal-body"><p>Failed to log in. Please make sure you have the correct login information.</p></div><div class="modal-footer"><button class="btn btn-primary" type="button" id="close_modal_button">Close</button></div></div></div></div>'); 
        $('body').find("#failed_login_modal").modal('show');   

        $('body').find("#failed_login_modal").find("#close_modal_button").on('click', function(){
            $('body').find("#failed_login_modal").modal("hide");
        });

    }
}
