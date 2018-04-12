if(window.location.href.includes("login")){
    $('body').find("#failed_login_modal").find("#close_modal_button").on('click', function(){
        console.log("hihihih");
        $('body').find("#failed_login_modal").modal("hide");
    });
}