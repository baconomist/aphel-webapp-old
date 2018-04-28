if(window.location.href.includes("add_student"))
{
    server_bridge.sendToServer("", {"function": "get_students"}, function(response){
        students = response["data"];
        
        for(i = 0; i < students.length; i++)
        {
            students[i] = "<option value=" + students[i] + "></option>";
        }
        
        $("<datalist id='student_list'>" + students + "</datalist>").insertAfter("#student_name")
    });
    
    $("#add_btn").click(function(){
        server_bridge.sendToServer("", {"function": "add_student_to_teacher", "data": {"student_name": $("#student_name").val(),
                                                                                       "login": JSON.parse(getCookie("login"))} },
           function(response)
           {
                location.replace(server_bridge.host + "/students");
           });
    });
}