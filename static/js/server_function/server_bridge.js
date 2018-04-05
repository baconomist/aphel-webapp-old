

class ServerBridge {
  constructor() {
    var protocol = location.protocol;
    var slashes = protocol.concat("//");
    this.host = slashes.concat(window.location.hostname);
    console.log(this.host);
  }

  sendToServer(url_ext, data, callback)
  {
    console.log("Sending data...");
    $.post(this.host + url_ext, data, function (status){
        console.log("Sent data:" + data);
        console.log("Status:" + status);
        callback(status);
    });
      
  }

  getFromServer(url_ext, data, callback)
  {
    console.log("Getting data...");
    $.get(this.host + url_ext, data, function(response){
        console.log("Received get response:" + response);
        callback(response);
    });
  }

}
