const slider = document.getElementById("my_opinion");
const output = document.getElementById("current_opinion");
slider.oninput = function() {output.innerHTML = this.value;}