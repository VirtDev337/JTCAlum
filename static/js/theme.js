let theme = localStorage.getItem('theme')

if(theme == null){
	setTheme('light')
}else{
	setTheme(theme)
}
// Activate the current theme (using class)
// body.classList = theme;
body.setAttribut('theme-style', theme);
// Available Themes
let available_themes = document.querySelectorAll('[theme-style]');
// let themeDots = document.getElementsByClassName('theme-dot')


for (var i=0; themeDots.length > i; i++){
	themeDots[i].addEventListener('click', function(){
		let mode = this.dataset.mode
		console.log('Option clicked:', mode)
		setTheme(mode)
	})
}

function setTheme(mode){
	// if(mode == 'light'){
	// 	document.getElementById('theme-style').href = 'app.css'
	// }

	// if(mode == 'dark'){
	// 	document.getElementById('theme-style').href = 'dark-app.css'
	// }
	
	// Toggle light / dark theme
    ( theme == 'light' ? theme = 'dark' : theme = 'light');
    // Apply class to body
    body.classList = theme;
    // Store theme var to localStorage
    

	window.localStorage.setItem('theme', mode)
}
