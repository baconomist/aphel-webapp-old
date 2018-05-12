class Navbar
{
    constructor()
    {
        this.layouts = {"not_logged_in": ["#nav_login", "#nav_register"], "logged_in": ["#nav_user"]}
    }

    update_layout(layout)
    {
        this.hide_all();

        let items_to_show = this.layouts[layout];
        for (let i = 0; i < items_to_show.length; i++)
        {
            $("#transmenu").find(items_to_show[i]).show();
            console.log(items_to_show[i]);
        }
    }

    hide_all()
    {
        $("#nav_login").hide();
        $("#nav_register").hide();
        $("#nav_user").hide();
    }

}

$(document).ready(function ()
{
    // Call function twice to make sure the navbar is updated
    check_navbar();
});

function check_navbar()
{
    navbar = new Navbar();

    //If login cookie null
    try
    {
        navbar.update_layout("logged_in");

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

                if(response["data"] >= 1)
                {
                    $(".auth-for-post").show();
                }

            });

    }
    catch
    {
        navbar.update_layout("not_logged_in");
    }
}




