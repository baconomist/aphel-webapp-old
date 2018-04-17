if(window.location.href.includes("dashboard")){
div = $("#dashboard");

server_bridge.sendToServer("/", { "function": "get_dashboard" }, function(response){
    //div.html(response["data"]);
    response["data"] = response["data"].reverse();
    for(i = 0; i < response["data"].length; i++)
    {
        console.log(response["data"][i])
        div.append("<div>" + "<p>"  + JSON.parse(response["data"][i])["user_name"] + ":</p>" + JSON.parse(response["data"][i])["content_html"] + "</div>")
    }
});  
}