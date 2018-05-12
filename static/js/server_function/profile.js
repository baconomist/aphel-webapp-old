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

    let profile_image = document.getElementById('profile_image').files[0];
    let reader = new FileReader();
    reader.addEventListener('load', function (event)
    {
        console.log("adasdadad", event.target.result);

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

                //location.replace(server_bridge.host + "/profile");
            });


        $.ajax({
            url: server_bridge.host+"/file_upload",
            type: "POST",
            dataType: "binary",
            processData: false,
            data: event.target.result,
            crossOrigin: true,
            success: function(result){
                // do something with binary data
            }
        });

    });

    reader.readAsArrayBuffer(profile_image);


    //location.replace(server_bridge.host + "/profile");
    return false;
});


