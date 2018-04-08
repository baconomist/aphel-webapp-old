div = $("#dashboard");

server_bridge.sendToServer("/dashboard", data=null, function(response){
    div.html(response["data"]);
});  