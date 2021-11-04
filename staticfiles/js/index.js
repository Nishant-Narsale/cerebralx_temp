
console.log('javascript working');
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

var homeContainer = document.getElementById("home");
var infoContainer1 = document.getElementById("InfoContainer1");
var infoContainer2 = document.getElementById("InfoContainer2");
var ServicesContainer = document.getElementById("ServicesContainer");
var infoContainer4 = document.getElementById("InfoContainer4");


function elementInViewport(el) {
    var top = el.offsetTop;
    var left = el.offsetLeft;
    var width = el.offsetWidth;
    var height = el.offsetHeight;
  
    while(el.offsetParent) {
      el = el.offsetParent;
      top += el.offsetTop;
      left += el.offsetLeft;
    }
  
    return (
      top < (window.pageYOffset + window.innerHeight) &&
      left < (window.pageXOffset + window.innerWidth) &&
      (top + height) > window.pageYOffset &&
      (left + width) > window.pageXOffset
    );
}

window.addEventListener('scroll', function() {
    if(window.pageYOffset >= 100){
        document.getElementsByClassName('Nav')[0].style.background = '#000';
    }else{
        document.getElementsByClassName('Nav')[0].style.background = 'transparent';
    }

    
    if( elementInViewport(infoContainer1) && !elementInViewport(homeContainer)) {
        document.getElementById("about").style.borderBottom = "3px solid #01bf71";
    }else{
        document.getElementById("about").style.borderBottom = "0px";
    }
    if( elementInViewport(infoContainer2) && !elementInViewport(infoContainer1) ) {
        document.getElementById("discover").style.borderBottom = "3px solid #01bf71";
    }else{
        document.getElementById("discover").style.borderBottom = "0px";
    }
    if( elementInViewport(ServicesContainer) && !elementInViewport(infoContainer2) ) {
        document.getElementById("services").style.borderBottom = "3px solid #01bf71";
    }else{
        document.getElementById("services").style.borderBottom = "0px";
    }
    if( elementInViewport(infoContainer4) && !elementInViewport(ServicesContainer) ) {
        document.getElementById("signup").style.borderBottom = "3px solid #01bf71";
    }else{
        document.getElementById("signup").style.borderBottom = "0px";
    }
});




