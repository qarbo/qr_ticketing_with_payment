var pushButton = document.getElementById('push-button');
var playground = document.getElementById('playground');
var menuground = document.getElementById('menuground');
var main = document.getElementById('main');
var pgPushed = false;
var menuPushed = false;
var playgroundWidth = playground.offsetWidth;
var menugroundWidth = menuground.offsetWidth;
const toggleButton = document.getElementById('toggle-button');
const hiddenContent = document.getElementById('restaurant-map');

function pushField() {
    playgroundWidth = playground.offsetWidth;
    if (pgPushed) {
        playground.style.right = -playgroundWidth - 400 + 'px';
        /*main.style.left = 0;
        main.style.right = 0;*/
        pgPushed = false;
    }
    else {
        if (menuPushed) {
            pushMenu();
        }
        playground.style.right = 0;
        /*main.style.left = -playgroundWidth + 'px';
        main.style.right = playgroundWidth + 'px';*/
        pgPushed = true;
        console.log (pushed);
        main.style.filter = 'blur(1px)';
    }
}

function pushMenu() {
    menugroundWidth = menuground.offsetWidth;
    if (menuPushed) {
        menuground.style.left = -menugroundWidth - 400 + 'px';
        menuPushed = false;
    }
    else {
        if (pgPushed){
            pushField();
        }
        menuground.style.left = 0;
        menuPushed = true;
        console.log (pushed);
    }

}

toggleButton.addEventListener('click', () => {
    if (hiddenContent.style.display === 'none') {
        hiddenContent.style.display = 'block';
    } else {
        hiddenContent.style.display = 'none';
    }
});


function logoButton() {
    if (pgPushed){
        pushField();
    }
    if (menuPushed) {
        pushMenu();
    }
}