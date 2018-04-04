// Stop button redirect,
// return false so its as if button was not clicked
/*$("#signup_button").on("click", function(){
    if()
    return false;
});*/

$("#signup_form").on("submit", function(){
   // get all the inputs into an array.
    var inputs = $('#signup_form :input');

    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    inputs.each(function() {
        values[this.name] = $(this).val();
    });
    
    if(values["password"].length > 6 && values["password"] == values["password-repeat"]){
        console.log("Signing up!")
        return server_bridge.sendToServer("/signup", values);
    }
    
    // Don't post to server
    return false;
    
});
  