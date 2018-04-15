#DOCS FOR APHEL WEBAPP

####Author: Lucas Borowiecki

###COMMUNICATION SYNTAX:

##POST SYNTAX:
	{
	"function":"a function(ie signup)",
	"data":"any parameters for said function"
	}
	
##SERVER RESPONSE SYNTAX:
	{
	"data": "response data used by client",
	"status": "status of request(error(detailed error)" or "success(succesfully **completed function**))"
	}
		
##REQUEST HANDLING:
	#Create request handler instance
	request_handler = RequestHandler()
    @app.route("/", defaults={"path": ""})
    @app.route('/<path:path>')
    def catch_all(path):
		request_handler.handle_request()

	
