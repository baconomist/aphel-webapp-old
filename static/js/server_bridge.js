

class ServerBridge {
  constructor() {
    var protocol = location.protocol;
    var slashes = protocol.concat("//");
    this.host = slashes.concat(window.location.hostname);
    console.log(this.host);
  }

  sendToServer(url_ext, data)
  {
    $.post(this.host + url_ext, data, function (status){
      console.log("Sent data:" + data);
      console.log("Status:" + status)
    });
  }

  getFromServer(url_ext, dataa)
  {

    $.ajax({
      url: this.host + url_ext,
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
