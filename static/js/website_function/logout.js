if(window.location.href.includes("logout"))
{
    eraseCookie("login");
    console.log("Successfully logged out!")
}