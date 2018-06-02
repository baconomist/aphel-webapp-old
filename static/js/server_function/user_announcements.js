if(window.location.href.includes("user_")){
   
    //$('body').find("#announcement_template").hide();
    
    login_check();
    
    server_bridge.sendToServer("/", {"function": "get_announcements_for_user"}, function(response){
        console.log(response)
        console.log(response["data"])
        response["data"] = response["data"].reverse();
        for(i=0; i < response["data"].length; i++){
            createShowableAnnouncement(JSON.parse(response["data"][i]));
        }
    });
}



function createShowableAnnouncement(announcement)
{
    
    num_id = announcement["id"]
    
    clone = constructShowableAnnouncement(announcement, num_id);
    
    // Need to get new reference to clone
    clone = $('#announcement_div').append(clone);

    clone.find("#edit_button"+num_id).click(function(event){
        num_id = parseInt(event.target.id.replace("edit_button", ""))
        createEditableAnnouncement(announcement, $("#announcement_not_editing"+num_id), num_id);
    });
    clone.find("#delete_button"+num_id).click(function(){
        deleteAnnouncement(announcement);
    });
    
    
}

function constructShowableAnnouncement(announcement, num_id)
{
    clone = $('body').find("#announcement_not_editing").clone();                
                        
    // Unhide object since it was hidden earlier
    clone.show();
    
    clone.find("#announcement_title").html(announcement["title"]);
    clone.find("#announcement_info").html(announcement["info"]);
    clone.find("#announcement_time_stamp").html(announcement["time_stamp"]);
    clone.find("#announcement_content").html(announcement["content_html"]);
    
    clone.attr("id", "announcement_not_editing"+num_id);
    
    // Make all child element ids unique, you can't have duplicate ids anywhere in the document.
    recursive_id_change(clone, num_id);    
    
    return clone;
}


function createEditableAnnouncement(announcement, showableAnnouncement, num_id)
{
    clone = $("#announcement_editing").clone();
    clone.show();
    
    clone.find("#announcement_edit_title").val(announcement["title"]);
    clone.find("#announcement_edit_info").val(announcement["info"]);
    
    clone.attr("id", "announcement_editing"+num_id);
    recursive_id_change(clone, num_id)
    
    console.log(showableAnnouncement);
    clone = clone.insertBefore(showableAnnouncement);
    showableAnnouncement.remove();
    
    div = clone.find("#announcement_editor_div"+num_id);
    div.html(announcement["content_html"]);
    
    var announcement_editor = new AnnouncementEditor(div, announcement["id"]);
    
    clone.find("#save_button"+num_id).click(function(){
        
        title = clone.find("#announcement_edit_title"+num_id).val()
        info = clone.find("#announcement_edit_info"+num_id).val()
        content_html = announcement_editor.get_content();
        id = announcement["id"];
        
        server_bridge.sendToServer("", {"function": "save_announcement", "data": {"announcement_data": {"title": title, "info": info, "content_html": content_html, "id": id} } },
               function(response){
                    console.log("Edited Announcement!");
        });
        
        announcement["title"] = clone.find("#announcement_edit_title" + num_id).val()
        announcement["info"] = clone.find("#announcement_edit_info" + num_id).val()
        announcement["content_html"] = announcement_editor.get_content();
        
        showableAnnClone = constructShowableAnnouncement(announcement, num_id);
        showableAnnClone = showableAnnClone.insertBefore($("#announcement_editing"+num_id));
        
        showableAnnClone.find("#edit_button"+num_id).click(function(event){
            num_id = parseInt(event.target.id.replace("edit_button", ""))
            createEditableAnnouncement(announcement, $("#announcement_not_editing"+num_id), num_id);
        });
        showableAnnClone.find("#delete_button"+num_id).click(function(){
            deleteAnnouncement(announcement);
        });

        $("#announcement_editing"+num_id).remove();
        
        console.log("done");
    });
    
}




function deleteAnnouncement(announcement)
{
    console.log("delete");
    server_bridge.sendToServer("", {"function": "delete_announcement", 
                                    "data": {"announcement_id": announcement["id"]}},
        function(response){
            deleteEditableAnnouncementById(announcement["id"]);
        }

    );
}


function deleteEditableAnnouncementById(id)
{
    for(i = 0; i < $("#announcement_div").children().length; i++)
    {
        child = $($("#announcement_div").children()[i]);
        num_id = parseInt(child.attr("id").replace("announcement_not_editing", ""));
        console.log(child);
        if(num_id == id)
        {
            child.remove();
        }
        
    }    
}





















