class Navbar
{
    constructor()
    {
        this.layouts = {"not_logged_in": ["#nav_login", "#nav_register"], "logged_in": ["#nav_user"]}
    }

    update_layout(layout)
    {
        let items_to_show = this.layouts[layout];
        for (let i = 0; i < items_to_show.length; i++)
        {
            $("#transmenu").find(items_to_show[i]).show();
        }
    }

}

$(document).ready(function ()
{
    navbar = new Navbar();
    is_user_logged_in(function (is_logged_in)
    {
        if (is_logged_in)
        {
            navbar.update_layout("logged_in");
        }
        else
        {
            navbar.update_layout("not_logged_in");
        }
    });

    if(getCookie("login") != null)
    {
        server_bridge.sendToServer("", {
                "function": "get_user_permission_level",
                "data": {"email": JSON.parse(getCookie("login"))["email"]}
            },
            function (response)
            {
                console.log(response["data"]);
                if (response["data"] >= 3)
                {
                    $(".admin").show();
                }

            });
    }

});




