

$("#login_form").on("submit", function(){
    
    console.log("Logging in...");
    
    // get all the inputs into an array.
    var inputs = $('#login_form :input');
    
    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    inputs.each(function() {
        values[this.id] = $(this).val();
    });
    
    console.log("Password: " + values["password"] + " Email: " + values["email"]);
    
    
    server_bridge.sendToServer("/login", values);
    
    // Don't post to server
    return false;
    
});
  