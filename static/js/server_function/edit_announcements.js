if(window.location.href.includes("edit_announcements")){
    server_bridge.sendToServer("/dashboard", data=null, function(response){
        //div.html(response["data"]);
        for(i = 0; i < response["data"].length; i++)
        {
            $(this).append("<div id=editor" + i + "></div>")
            div = $(this).append()
            console.log(response["data"][i])
            div.append("<div>" + JSON.parse(response["data"][i])["content_html"] + "</div>")
        }
    });  
}