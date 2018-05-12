if(window.location.href.includes("logout"))
{
    eraseCookie("login");
    setCookie("login", null);
    console.log("Successfully logged out!")
}