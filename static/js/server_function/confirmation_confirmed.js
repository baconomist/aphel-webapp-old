if(window.location.href.includes("confirmation_confirmed"))
{
    server_bridge.sendToServer("", {"function": "validate_confirmation", "data": {"confirmation_id": getParameterByName("id")} }, function(response){
        if(response["data"])
        {
            console.log("Confirmation Confirmed!");
        }
        else
        {
            $("#confirmation_confirmed_status").text("Confirmation Link Invalid!");
            $("#confirmation_confirmed_login").text("");
            
            console.log("Confirmation Link Invalid!");
        }
    });
}
    
                               
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}