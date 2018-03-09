class RequestHandler(object):
    def __init__(self):
        self.actions = {"/login": self.login, "/isUserAdmin": self.is_user_admin,
                        "/isUserAuthForPost": self.is_user_auth_for_post}

    def handle_request(self, request, url_ext):
        self.actions[url_ext](request)

    def login(self, request):
        assert b'The request method for login was not "POST"!', request.method == "POST"


    def is_user_admin(self, request):
        pass

    def is_user_auth_for_post(self, request):
        pass
