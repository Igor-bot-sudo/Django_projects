function fadeIn(el) {
    let opacity = 0.1;
    let timer = setInterval(function() {
        if(opacity >= 1) {
            clearInterval(timer);
        }
        el.style.opacity = opacity;
        opacity += opacity * 0.1;
    }, 5);
}

window.onload = window.onpageshow = function(){
    fadeIn(document.body)
}
