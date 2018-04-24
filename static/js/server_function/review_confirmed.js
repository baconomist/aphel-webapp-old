if(window.location.href.includes("review_confirmed"))
{
    server_bridge.sendToServer("", {"function": "validate_review", "data": {"review_id": getParameterByName("id")} }, function(response){
        if(response["data"])
        {
            console.log("Review Confirmed!");
        }
        else
        {
            $("#review_status").text("Review Invalid!");
            
            console.log("Review Invalid!");
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