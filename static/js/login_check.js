function login_check()
{
    var body = $("body");

    if (JSON.parse(getCookie("login")) != null)
    {
        server_bridge.sendToServer("/login", JSON.parse(getCookie("login")), function (response) {
            if (response["data"])
            {
                console.log("**login_check** Logged in.");
            }
            else
            {
                console.log("**login_check** Not logged in!");

                body.append('<div role="dialog" tabindex="-1" class="modal fade" id="failed_login_modal"><div class="modal-dialog modal-dialog-centered" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button></div><div class="modal-body"><p>Failed to log in. Please make sure you have the correct login information.</p></div><div class="modal-footer"><button class="btn btn-primary" type="button" id="close_modal_button">Close</button></div></div></div></div>');
                body.find("#failed_login_modal").modal('show');

                body.find("#failed_login_modal").find("#close_modal_button").on('click', function () {
                    body.find("#failed_login_modal").modal("hide");
                });

            }
        });
    }
    else
    {
        console.log("**login_check** Not logged in!");

        body.append('<div role="dialog" tabindex="-1" class="modal fade" id="failed_login_modal"><div class="modal-dialog modal-dialog-centered" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">×</span></button></div><div class="modal-body"><p>Failed to log in. Please make sure you have the correct login information.</p></div><div class="modal-footer"><button class="btn btn-primary" type="button" id="close_modal_button">Close</button></div></div></div></div>');
        body.find("#failed_login_modal").modal('show');

        body.find("#failed_login_modal").find("#close_modal_button").on('click', function () {
            body.find("#failed_login_modal").modal("hide");
        });

    }
}