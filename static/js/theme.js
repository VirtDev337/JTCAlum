// let theme = localStorage.getItem('theme')

// if(theme == null){
// 	setTheme('light')
// }else{
// 	setTheme(theme)
// }
// // Activate the current theme (using class)
// // body.classList = theme;
// body.setAttribut('color-theme', theme);
// // Available Themes
// let available_themes = document.querySelectorAll('[color-theme]');
// // let themeDots = document.getElementsByClassName('theme-dot')


// for (var i=0; themeDots.length > i; i++){
// 	themeDots[i].addEventListener('click', function(){
// 		let mode = this.dataset.mode
// 		console.log('Option clicked:', mode)
// 		setTheme(mode)
// 	})
// }

// function setTheme(mode){
// 	// if(mode == 'light'){
// 	// 	document.getElementById('theme-style').href = 'app.css'
// 	// }

// 	// if(mode == 'dark'){
// 	// 	document.getElementById('theme-style').href = 'dark-app.css'
// 	// }
	
// 	// Toggle light / dark theme
//     ( theme == 'light' ? theme = 'dark' : theme = 'light');
//     // Apply class to body
//     body.classList = theme;
//     // Store theme var to localStorage
    

// 	window.localStorage.setItem('theme', mode)
// }

// **********************************************// from https://dev.to/mritunjaysaha/theme-switching-using-local-storage-13i

const themeSwitcher = document.getElementById("theme-switch");

themeSwitcher.checked = false;

function clickHandler() {
	if (this.checked) {
		document.body.classList.remove("light");
		document.body.classList.add("dark");
		localStorage.setItem("theme", "dark");
	} else {
		document.body.classList.add("light");
		document.body.classList.remove("dark");
		localStorage.setItem("theme", "light");
	}
}
themeSwitcher.addEventListener("click", clickHandler);

window.onload = checkTheme();

function checkTheme() {
    const localStorageTheme = localStorage.getItem("theme");

    if (localStorageTheme !== null && localStorageTheme === "dark") {
        // set the theme of body
        document.body.className = localStorageTheme;

        // adjust the slider position
        const themeSwitch = document.getElementById("theme-switch");
        themeSwitch.checked = true;
    }
}
