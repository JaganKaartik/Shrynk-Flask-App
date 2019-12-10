function toggleURL(value)
{
    if(value.localeCompare('url')==0)
    {
        var x = document.getElementById("addurlform");
    }
    else
    {
        var x = document.getElementById("dash");
    }
    if (x.style.display === "none") { x.style.display = "block";} 
    else { x.style.display = "none";}
}
