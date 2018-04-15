if(window.location.href.includes("user_announcements")){
   
    $('body').find("#announcement_template").hide();
    
    login_check();
    
    server_bridge.sendToServer("/", {"function": "get_announcements_for_user", "data":JSON.parse(getCookie("login"))["email"]}, function(response){ 
        response["data"] = response["data"].reverse();
        for(i=0; i < response["data"].length; i++){
            createEditableAnnouncement(JSON.parse(response["data"][i]));
        }
    });
}

var x = 0;

function createEditableAnnouncement(announcement)
{
    
    
    // If element exists, else...
    if($('body').find("#announcement_template").length > 0)
    {
        clone = $('body').find("#announcement_template").clone();
        // Remove old template to stop interference with onClick events
        //$('body').find("#announcement_template").remove();
    }
    else
    {
        clone = $('body').find("#announcement_card"+(x-1)).clone();
    }
    
    // Make all child element ids unique, you can't have duplicate ids anywhere in the document.
    (function recursiveChildren(element)
    {
        element.children().each(function () {
            if(this.id.length > 0)
            {
                this.id = this.id + x;
                console.log(this.id);
            }
            jQueryElement = $(this);
            recursiveChildren(jQueryElement);
        });
    })(clone);
    
    // Unhide object since it was hidden earlier
    clone.show();
        
    clone.find("#content_html"+x).html(announcement["content_html"]);
    
    clone.attr("id", "announcement_card"+x);
    
    // Need to get new reference to clone
    clone = $('body').append(clone);

    clone.find("#edit_button"+x).click(function(event){
        num = parseInt(event.target.id.replace("edit_button", ""))
        div = clone.find("#content_html"+num).parent();
        div.attr("id", "editor"+num);
        createEditArea(div, announcement);
    });
    clone.find("#delete_button"+x).click(function(){
        deleteAnnouncement(announcement);
    });
    
    x++;
    
}

function createEditArea(div, announcement)
{
    console.log("edit");
    init_quill(div, announcement["id"]);
}


function deleteAnnouncement(announcement)
{
    console.log("delete");
    server_bridge.sendToServer("", {"function": "delete_announcement", 
                                    "data": {"login":JSON.parse(getCookie("login")), "announcement_id": announcement["id"]}}, 
        function(response){
            location.reload();
        }

    );
}






















