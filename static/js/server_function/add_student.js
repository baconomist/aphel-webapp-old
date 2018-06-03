if(window.location.href.includes("add_student"))
{
    $("#add_btn").click(function(){
        server_bridge.sendToServer("", {"function": "add_student_to_teacher", "data": {"student_name": $("#student_name").val(),
                                                                                       "login": JSON.parse(getCookie("login"))} },
           function(response)
           {
                location.replace(server_bridge.host + "/students");
           });
    });
}