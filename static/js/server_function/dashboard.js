if(window.location.href.includes("dashboard")){
    div = $("#dashboard");

    server_bridge.sendToServer("/", { "function": "get_dashboard" }, function(response){
        //div.html(response["data"]);
        response["data"] = response["data"].reverse();
        for(i = 0; i < response["data"].length; i++)
        {
            create_announcement(JSON.parse(response["data"][i]));
        }
    });  
}

x = 0;

function create_announcement(announcement_data)
{    
    // id can't be "announcement_template" or else the element doesn't show up!
    clone = $("#dashboard_announcement_template").clone();
    clone.show();
    // clone.find("#announcement_title").text(announcement_data["title"]);
    clone.find("#announcement_info").text("User: " + announcement_data["user_name"]);
    clone.find("#announcement_content").html("Content: " + announcement_data["content_html"]);
    clone.find("#announcement_time_stamp").text("TimeStamp: " + announcement_data["time_stamp"]);
    
    clone.attr("id", "dashboard_announcement"+x)
    
    recursive_id_change(clone, x);
    console.log("aaaa");
    
    clone = $("#dashboard_div").append(clone);
    clone.show();
    console.log(clone);
    
    console.log(announcement_data, announcement_data["time_stamp"], announcement_data["content_html"]);
    
    x++;
}