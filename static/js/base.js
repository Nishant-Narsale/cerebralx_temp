var isOpen = false

function Toggle(){
    if(!isOpen){
        document.getElementsByClassName("SidebarContainer")[0].style.opacity = "100%";
        document.getElementsByClassName("SidebarContainer")[0].style.top = "0";
    }else{
        document.getElementsByClassName("SidebarContainer")[0].style.opacity = "0%";
        document.getElementsByClassName("SidebarContainer")[0].style.top = "-100%";
    }
    isOpen = !isOpen;
}