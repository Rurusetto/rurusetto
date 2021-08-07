window.onscroll = function() {scrollFunction()};
window.onresize = function() {onResize()};
window.addEventListener('load', function() {scrollFunction()})

header = document.getElementById("header")
profilePicture = document.getElementById("profile-picture")
headerLogo = document.getElementById("header-logo")
navListing = document.getElementById("nav-listing")
navInstall = document.getElementById("nav-install")
navStatus = document.getElementById("nav-status")
navChangelog = document.getElementById("nav-changelog")

mobileHeader = document.getElementById("mobile-header")
mobileLogo = document.getElementById("mobile-logo")
arrowProfileMenu = document.getElementById("arrow-profile-menu")

function scrollFunction() {
    if (document.documentElement.clientWidth >= 1010) {
        if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
            profilePicture.style.height = "32px";
            profilePicture.style.width = "32px";
            headerLogo.style.height = "50px";
            header.style.backgroundColor = "rgba(74,74,74,.8)"
            header.classList.add('blur-bg')
            navListing.style.fontSize = "18px"
            navInstall.style.fontSize = "18px"
            navStatus.style.fontSize = "18px"
            navChangelog.style.fontSize = "18px"
        } else {
            profilePicture.style.height = "48px";
            profilePicture.style.width = "48px";
            headerLogo.style.height = "65px";
            header.style.backgroundColor = "rgba(74,74,74,0)"
            header.classList.remove('blur-bg')
            navListing.style.fontSize = "20px"
            navInstall.style.fontSize = "20px"
            navStatus.style.fontSize = "20px"
            navChangelog.style.fontSize = "20px"
        }
    } else {
        if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
            mobileHeader.style.height = "7%";
            mobileHeader.style.minHeight = "68px";
            mobileLogo.style.marginTop = "-5px";
            mobileLogo.style.marginLeft = "-5px";
            mobileLogo.style.height = "45px";
            mobileHeader.style.backgroundColor = "rgba(74,74,74,.8)";
            mobileHeader.classList.add('blur-bg');
            document.getElementById("navbarToggleExternalContent").style.marginTop = "68px";
        } else {
            mobileHeader.style.height = "8%";
            mobileHeader.style.minHeight = "75px";
            mobileLogo.style.marginTop = "0";
            mobileLogo.style.marginLeft = "0";
            mobileLogo.style.height = "50px";
            mobileHeader.style.backgroundColor = "rgba(74,74,74,0)";
            mobileHeader.classList.remove('blur-bg');
            document.getElementById("navbarToggleExternalContent").style.marginTop = "77px";
        }
    }
}

function onResize() {
    if (document.documentElement.clientWidth >= 1010) {
        header.classList.add('show')
        header.classList.remove('hidden')
        header.style.zIndex = "2"
        mobileHeader.style.zIndex = "0"
        profilePicture.style.zIndex = "2"
        headerLogo.style.zIndex = "2"
        navListing.classList.remove('disabled')
        navInstall.classList.remove('disabled')
        navStatus.classList.remove('disabled')
        navChangelog.classList.remove('disabled')
        profilePicture.classList.remove('disabled')
        headerLogo.classList.remove('disabled')
    } else {
        header.classList.add('hidden')
        header.classList.remove('show')
        header.style.zIndex = "0"
        mobileHeader.style.zIndex = "2"
        profilePicture.style.zIndex = "0"
        headerLogo.style.zIndex = "0"
        navListing.classList.add('disabled')
        navInstall.classList.add('disabled')
        navStatus.classList.add('disabled')
        navChangelog.classList.add('disabled')
        profilePicture.classList.add('disabled')
        headerLogo.classList.add('disabled')
    }
    if (document.documentElement.clientWidth >= 1010 && header.classList.contains('hidden')) {
        header.classList.remove('hidden');
    }

    if ((document.documentElement.clientWidth < 1010 && header.style.backgroundColor === "rgba(74,74,74,0.8)") ||
        (document.documentElement.clientWidth < 1010 && header.classList.contains('show'))) {
        header.style.backgroundColor = "rgba(74,74,74,0)";
    }

    if (document.documentElement.clientWidth < 1010 && header.classList.contains('show')) {
        header.classList.add('hidden');
    }
    scrollFunction()
}

function rotateArrowMenu() {
    if (document.getElementById("profile-menu").getAttribute("aria-expanded") === "false" || arrowProfileMenu.classList.contains('fa-chevron-down')) {
        arrowProfileMenu.classList.remove('fa-chevron-down')
        arrowProfileMenu.classList.add('fa-chevron-up')
    } else {
        arrowProfileMenu.classList.remove('fa-chevron-up')
        arrowProfileMenu.classList.add('fa-chevron-down')
    }
}

window.addEventListener("load", function(){onResize()})

function copyToClipboard(text) {
    let input = document.body.appendChild(document.createElement("input"));
    input.value = text;
    input.focus();
    input.select();
    document.execCommand('copy');
    input.parentNode.removeChild(input);
    window.alert("Copied!")
}