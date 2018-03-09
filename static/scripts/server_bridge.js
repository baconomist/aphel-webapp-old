

class ServerBridge {
  constructor() {
    var protocol = location.protocol;
    var slashes = protocol.concat("//");
    this.host = slashes.concat(window.location.hostname);
    console.log(this.host);
  }

  sendToServer(data)
  {
    $.post(this.host, data, function (status){
      console.log("Sent data:" + data);
      console.log("Status:" + status)
    });
  }

  getFromServer(dataa)
  {

    $.ajax({
      url: this.host,
      type: "get", //send it through get method
      data: dataa,
      success: function(response) {
        //Do Something
        console.log("Got data:" + response);
      },
      error: function(xhr) {
        //Do Something to handle error
        console.log("Got data:" + xhr);
      }
    });
  }

}
