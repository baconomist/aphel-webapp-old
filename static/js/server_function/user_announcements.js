if(window.location.href.includes("user_announcements")){
   
    $('body').find("#announcement_template").hide();
    
    login_check();
    
    server_bridge.sendToServer("/", {"function": "get_announcements_for_user", "data":JSON.parse(getCookie("login"))["email"]}, function(response){ 
        response["data"] = response["data"].reverse();
        for(i=0; i < response["data"].length; i++){
            clone = $('body').find("#announcement_template").clone();
            clone.find("#content_html").html(JSON.parse(response["data"][i])["content_html"]);
            $('body').append(clone.html());
        }
    });
}