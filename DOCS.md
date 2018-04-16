#DOCS FOR APHEL WEBAPP

####Author: Lucas Borowiecki

## COMMUNICATION SYNTAX ##

### POST SYNTAX ###
	{
	"function":"a function(ie signup)",
	"data":"any parameters for said function"
	}

#### User Info Syntax ####
	{
	"data": 
		{
		"login": 
			{
			"email": value,
			"password": value
			}
		}
	}
	
### SERVER RESPONSE SYNTAX ###
	{
	"data": "response data used by client",
	"status": "status of request(error(detailed error)" or "success(succesfully **completed function**))"
	}
		
## REQUEST HANDLING ##
	#Create request handler instance
	request_handler = RequestHandler()
    @app.route("/", methods=["POST"])
    def catch_all(path):
		request_handler.handle_request()




	
