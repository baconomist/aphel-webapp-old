if(window.location.href.includes("logout"))
{
    eraseCookie("login");
    setCookie("login", null);
}