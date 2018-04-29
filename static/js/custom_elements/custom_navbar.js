class FileBag extends HTMLElement {
    constructor(){
        super();

        this.innerHTML = '<nav class="navbar navbar-light navbar-expand-lg fixed-top bg-white transparency border-bottom border-light" id="transmenu" style="color:rgb(255,255,255);background-color:#439d4c;">\n' +
            '                    <div class="container"><a class="navbar-brand text-success" href="index.html" style="font-family:\'News Cycle\', sans-serif;font-size:39px;">&nbsp;<img class="img-fluid" src="../static/img/Aphel_icon.png" alt="Aphel Technologies" width="97px" height="97px" style="padding-right:0px;margin-right:10px;margin-bottom:7px;"></a>\n' +
            '                        <button class="navbar-toggler collapsed" data-toggle="collapse" data-target="#navcol-1"><span></span><span></span><span></span></button>\n' +
            '                            <div class="collapse navbar-collapse" id="navcol-1" style="font-family:\'News Cycle\', sans-serif;font-size:22px;">\n' +
            '                                <ul class="nav navbar-nav ml-auto">\n' +
            '                                    <li class="dropdown"><a class="dropdown-toggle nav-link dropdown-toggle" data-toggle="dropdown" aria-expanded="false" href="#" style="padding-right:20px;"><i class="fa fa-info-circle" style="padding-right:7px;"></i>Info</a>\n' +
            '                                        <div class="dropdown-menu" role="menu"><a class="dropdown-item" role="presentation" href="http://pchacks.ca/index.html#about"><i class="fa fa-handshake-o" style="padding-right:5px;"></i>About Us</a><a class="dropdown-item" role="presentation" href="http://pchacks.ca/index.html#contact"><i class="fa fa-volume-control-phone" style="padding-right:5px;"></i>Contact</a></div>\n' +
            '                                    </li>\n' +
            '                                    <li class="dropdown"><a class="dropdown-toggle nav-link dropdown-toggle" data-toggle="dropdown" aria-expanded="false" href="#" id="nav_user" style="padding-right:20px;display:none;"><i class="fa fa-user" style="padding-right:7px;"></i>User</a>\n' +
            '                                        <div class="dropdown-menu" role="menu">\n' +
            '                                            <a class="dropdown-item" role="presentation" href="profile.html">\n' +
            '                                                <i class="fa fa-address-card" style="padding-right:5px;"></i>Profile\n' +
            '                                            </a>\n' +
            '                                            <a class="dropdown-item" role="presentation" href="post_announcement.html">\n' +
            '                                                <i class="fa fa-envelope-open-o" style="padding-right:5px;"></i>Create Announcement\n' +
            '                                            </a>\n' +
            '                                            <a class="dropdown-item" role="presentation" href="user_announcements.html">\n' +
            '                                                <i class="fa fa-pencil"></i>&nbsp;Edit Announcements\n' +
            '                                            </a>\n' +
            '                                            <a class="dropdown-item admin" role="presentation" href="students.html" style="display:none">\n' +
            '                                                <i class="fa fa-book"></i>&nbsp;Manage Students\n' +
            '                                            </a>\n' +
            '                                            <a class="dropdown-item admin" role="presentation" href="add_student.html" style="display:none">\n' +
            '                                                <i class="fa fa-plus"></i><i class="fa fa-"></i>&nbsp;Add Student\n' +
            '                                            </a>\n' +
            '                                            <a class="dropdown-item" role="presentation" href="logout.html">\n' +
            '                                                <i class="fa fa-sign-out"></i>&nbsp;Logout\n' +
            '                                            </a>\n' +
            '                                        </div>\n' +
            '                                    </li>\n' +
            '                                    <li class="nav-item" role="presentation"><a class="nav-link" href="dashboard.html" style="padding-right:20px;"><i class="fa fa-tachometer" style="padding-right:7px;"></i>Dashboard</a></li>\n' +
            '                                    <li class="nav-item" role="presentation"><a class="nav-link" href="login.html" id="nav_login" style="padding-right: 20px; display: none;"><i class="fa fa-sign-in" style="padding-right:7px;"></i>Login</a></li>\n' +
            '                                    <li class="nav-item" role="presentation"><a class="nav-link" href="signup.html" id="nav_register" style="padding-right: 20px; display: none;"><i class="fa fa-wpforms" style="padding-right:7px;"></i>Register</a></li>\n' +
            '                                </ul>\n' +
            '                            </div>\n' +
            '                    </div>\n' +
            '                </nav>';

            this.id = "transbar";
    }
}

window.customElements.define('custom-nav', FileBag);