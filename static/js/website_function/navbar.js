class Navbar
{
    constructor()
    {
        this.layouts = {"logged_in": ["#nav_login", "#nav_register"], "not_logged_in": ["#nav_user"]}
    }    
    
    update_layout(layout)
    {
        this.unhide_all();
        var items_to_hide = this.layouts[layout]
        for(var i=0; i < items_to_hide.length; i++)
        {
            $("#transmenu").find(items_to_hide[i]).hide();  
                        console.log("aaaaa");
        }    
    }
    
    unhide_all()
    {
        $("#nav_login").show();
        $("#nav_register").show();
        $("#nav_user").show();
    }
}

$( document ).ready(function() {
    navbar = new Navbar();
    is_user_logged_in(function(is_logged_in){
        if(is_logged_in)
        {
            navbar.update_layout("logged_in");
        }
        else
        {
            navbar.update_layout("not_logged_in");
        }
    });

});




