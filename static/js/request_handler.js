
class RequestHandler 
{
    constructor(server_bridge)
    {
        this.server_bridge = server_bridge;
    }
    
    sendLogin(username, password)
    {
        console.log(SHA256(password).toString());
        
        this.server_bridge.sendToServer("/login", 
        {
            "username":username,
            "password":SHA256(password).toString()
        }
       );
        
    }
    
    sendSignup(username, password)
    {
        console.log(SHA256(password).toString());
        
        this.server_bridge.sendToServer("/signup",
        {
            "username":username,
            "password":SHA256(password).toString()
        }
       );    
        
    }



}