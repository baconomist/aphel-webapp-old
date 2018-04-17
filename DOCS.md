#DOCS FOR APHEL WEBAPP

####Author: Lucas Borowiecki

## COMMUNICATION SYNTAX ##

### POST SYNTAX ###
	{
	"function":"a function(ie signup)",
	"data":"any parameters for said function"
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

## maybe make the function syntax like {function:"function name", data:"function params named like function params on server"}



	
