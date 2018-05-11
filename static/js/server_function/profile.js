server_bridge.sendToServer("", {
        "function": "get_profile_data",
        "data": {"email": JSON.parse(getCookie("login"))["email"]}
    },
    function (response)
    {
        $("#firstname").html(response["data"]["firstname"]);
        $("#lastname").html(response["data"]["lastname"]);

        try
        {
            $("#grade").html(response["data"]["grade"]);
        }
        catch
        {
            console.log("Grade not found in profile data.")
            $("#grade").hide();
        }

    });

$("#profile_form").on("submit", function ()
{
    if ($("#grade").find(":selected").text() != null)
    {
        let grade = $("#grade").find(":selected").text();
    }

    server_bridge.sendToServer("", {
            "function": "save_profile_data",
            "data": {
                "login": JSON.parse(getCookie("login")),
                "firstname": $("#firstname").html(), "lastname": $("#lastname").html(),
                "grade": grade
            }
        },
        function (response)
        {
            console.log("Profile Successfully Saved!")
        });


    return false;
});


