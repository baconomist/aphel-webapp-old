# DOCS FOR APHEL WEBAPP #

#### Author(s): Lucas Borowiecki, Aryan Gosalia, The Apheltech Team ####

## COMMUNICATION SYNTAX ##

### POST SYNTAX ###
	{
	"function":"a function(ie signup)",
	"data":"any parameters for said function"
	}
	
### SERVER RESPONSE SYNTAX ###
	{
	"data": "response data used by client",
	"status": "status of request as a text"
	"status_code": "an integer status code from the list of custom status codes"
	}

## REQUEST HANDLING ##
	#Create request handler instance
	request_handler = RequestHandler()
    @app.route("/", methods=["POST"])
    def catch_all(path):
		request_handler.handle_request()


	
