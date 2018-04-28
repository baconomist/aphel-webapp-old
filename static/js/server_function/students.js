if(window.location.href.includes("students"))
{
    var student_options = $(".student-options").clone();
    
    server_bridge.sendToServer("", { "function": "get_teacher_students", "data": { "email": JSON.parse(getCookie("login"))["email"] } }, function(response){
        
        var student_uid;
        
        for(i = 0; i < response["data"].length; i++)
        {
            student_uid = response["data"][i];
            
            server_bridge.sendToServer("", { "function": "get_user_permission_level",
                                            "data": { "email": student_uid } },
            function(response){

                console.log(student_uid);
                createShowableStudent(student_uid, response["data"]);
            });
            
        }
        
        
    });
}

function createShowableStudent(student_uid, student_perm)
{
    clone = $(".student-template").clone();
    
    clone.show();

    clone.attr("student_uid", student_uid);
    clone.attr("student_perm", student_perm);
    
    clone.find(".student-name").text(student_uid);
    clone.find(".student-perm").html("Permission Level: " + student_perm);    

    createEventListenersForDropdown(clone);   

    $("#student_div").append(clone);
}
        
        
function createEditableStudent(clone)
{
    disableEditing(clone);
    
    clone.find(".student-options").remove();
    $("<tr> <th><h5 class=perm-edit-header>Permission Level: </h5></th> <th><select class='student-perm-input'></select></th> </tr>").insertBefore(clone.find(".student-perm"));
    
    clone.find(".student-perm-input").append("<option value='0'>" + 0 + "</option>");
    clone.find(".student-perm-input").append("<option value='1'>" + 1 + "</option>");
    clone.find(".student-perm-input").append("<option value='2'>" + 2 + "</option>");
    
    
    clone.find(".student-perm-input").children().each(function()
    {
        if(this.value.toString() == clone.attr("student_perm"))
        {
            this.selected = 'selected';
        }
    });
    
    createSaveButton(clone);
    
    clone.find(".student-perm").hide();
    
}

function disableEditing(clone)
{
    student_options.clone().appendTo(clone.find(".student-perm").parent().parent());
    
    createEventListenersForDropdown(clone);
    
    clone.find(".student-perm").html("Permission Level: " + clone.find(".student-perm-input").val());
    clone.attr("student_perm", clone.find(".student-perm-input").val());
    clone.find(".student-perm").show();
    
    clone.find(".student-perm-input").remove();
    clone.find(".save-btn").remove();
    
    clone.find(".perm-edit-header").remove();
}

function createEventListenersForDropdown(clone)
{
    clone.find(".student-edit").click(
    function()
    {
        createEditableStudent(clone);
    }
    );
    
    clone.find(".student-delete").click(
    function()
    {
        //IDK what this means exactly yet
        // Delete account or set user permission to 0 and stop managing user...
        //deleteStudent(clone);
        
        server_bridge.sendToServer("", {"function": "remove_student_from_teacher", "data": {"student_name": clone.attr("student_uid"),
                                                                                            "login": JSON.parse(getCookie("login"))} },
        function(response){
            clone.remove();
        });
    }
    ); 
}

function createSaveButton(clone)
{
    $('<button class="btn btn-primary save-btn" type="button" style="margin: 10px">Save</button>').insertAfter(clone.find(".student-perm"));
    $(".save-btn").click(function(){
        server_bridge.sendToServer("", {"function": "change_user_permission_level", "data": {"email": clone.attr("student_uid"), 
                                                                                             "permission_level": $(".student-perm-input").val(),
                                                                                            "login": JSON.parse(getCookie("login"))} },
                                                                                            function(response){});
        disableEditing(clone);
    });
}







