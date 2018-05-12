server_bridge.sendToServer("", {
        "function": "get_profile_data",
        "data": {"email": JSON.parse(getCookie("login"))["email"]}
    },
    function (response)
    {
        response["data"] = JSON.parse(response["data"]);

        $("#firstname").val(response["data"]["firstname"]);
        $("#lastname").val(response["data"]["lastname"]);

        $("#email").val(JSON.parse(getCookie("login"))["email"]);
        console.log(response["data"]["grade"]);
        if(response["data"]["grade"])
        {
            $("#grade_input").children().each(function()
            {
                if(this.value.toString() == response["data"]["grade"])
                {
                    this.selected = 'selected';
                    console.log("adada");
                }
            });
        }
        else
        {
            console.log("grade_input not found in profile data.");
            $("#grade_input").hide();
            $("#grade_label").hide();
        }

    });

$("#profile_form").on("submit", function ()
{
    let grade = 0;
    if ($("#grade_input").is(":visible"))
    {
        grade = $("#grade_input").val();
    }
    console.log("grade", grade);

    server_bridge.sendToServer("", {
            "function": "save_profile_data",
            "data": {
                "login": JSON.parse(getCookie("login")),
                "firstname": $("#firstname").val(), "lastname": $("#lastname").val(),
                "grade": grade
            }
        },
        function (response)
        {
            console.log("Profile Successfully Saved!")
        });

    location.replace(server_bridge.host + "/profile");
    return false;
});


