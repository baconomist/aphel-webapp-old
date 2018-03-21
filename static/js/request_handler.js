
class RequestHandler 
{
    constructor(server_bridge)
    {
        this.server_bridge = server_bridge;
    }
    
    sendLogin(username, password)
    {
        console.log(SHA256("hi").toString());
        this.server_bridge.sendToServer("/login", {
            "login":[username,
            SHA256("hi")]
        });
    }



}