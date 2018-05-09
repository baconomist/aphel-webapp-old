if(window.location.href.includes("announcement") && !window.location.href.includes("user")){
    
    server_bridge.sendToServer("", {"function": "get_teachers"}, function(response){
        teachers = response["data"];
        for(i = 0; i < teachers.length; i++)
        {
            teachers[i] = "<option value=" + teachers[i] + "></option>";
        }
        
        $("<datalist id='teacher_list'>" + teachers + "</datalist>").insertAfter(".ann-teacher")
    });
    
    
    announcement_id = 0
    server_bridge.sendToServer("", {"function": "get_new_announcement_id", "data": { "email": JSON.parse(getCookie("login"))["email"]} }, function(response){
        announcement_id = response["data"];
        
        console.log(announcement_id)
                
        server_bridge.sendToServer("", {"function": "is_user_auth_for_post_review", "data": { "email": JSON.parse(getCookie("login"))["email"] } }, function(response){
            is_user_auth_for_post_review = response["data"];
            
            server_bridge.sendToServer("", {"function": "is_user_auth_for_post", "data": { "email": JSON.parse(getCookie("login"))["email"] } }, function(response){
                is_user_auth_for_post = response["data"];
                
                if(is_user_auth_for_post)
                {
                    $(".ann-post-review").remove();
                    template = $(".ann-post");           
                }
                else if(is_user_auth_for_post_review)
                {
                    $(".ann-post").remove();
                    template = $(".ann-post-review");             
                }
                
                template.show();
                
                div = template.find("#editor");
                console.log(div);
                
                var announcement_editor = new AnnouncementEditor(div, announcement_id);
                
                template.find(".ann-post-btn").click(function(){
                    
                    title = template.find(".ann-title").val();
                    console.log(title);
                    info = template.find(".ann-info").val();
                    content_html = announcement_editor.get_content();
                    
                    teacher = template.find(".ann-teacher").val()
                    id = announcement_editor.announcement_id;
                    
                    server_bridge.sendToServer("", {"function": "save_announcement", "data": {"login": JSON.parse(getCookie("login")),
                                                                                         "announcement_data": {"title": title, "info": info,                                          "content_html": content_html, "teacher": teacher, "id": id} } },
                       function(response){
                            window.location.replace(server_bridge.host + "/dashboard");
                            console.log("Posted Announcement!");
                    });
                });
                
                
            });
        });
        
    });     
}


















