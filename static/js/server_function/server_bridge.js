

class ServerBridge
{
    constructor()
    {
        /*var protocol = location.protocol;
        var slashes = protocol.concat("//");
        this.host = slashes.concat(window.location.hostname);
        */

        // TEST HOST FOR FLASK SERVER!!!!!
        this.host = "http://localhost:80";

        this.sendToServer("/debug", {}, this.setHost.bind(this));

        let url = window.location.href;
        url = url.split("/");
        this.host = url[0] + "//" + url[2];
    }

    setHost(response)
    {
        if (!response["data"])
        {
            let url = window.location.href;
            url = url.split("/");
            this.host = url[0] + "//" + url[2];
        }
        else
        {
            this.host = "http://localhost:80";
        }
        console.log(this.host, "DEBUG: " + response["data"]);
    }

    sendToServer(url_ext, data, callback)
    {
        data = JSON.stringify(data);
        console.log("**ServerBridge** Sending data to: " + this.host + url_ext);
        $.post(this.host + url_ext, data)
            .done(
                function (response)
                {
                    console.log("Sent data:" + data);
                    console.log("**ServerBridge** Received Server Response: " + response);
                    callback(response);
                });
    }

    // This doesn't really work, doesn't post data. Just use sendToServer().

    /*getFromServer(url_ext, data, callback)
    {
      data = JSON.stringify(data);
      console.log("Getting data...");
      $.get(this.host + url_ext, data, function(response){
          console.log("**ServerBridge** Received GET response: " + response);
          callback(response);
}

      });
    }*/
    
}
    
