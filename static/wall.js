window.addEventListener('load', (event) => {
    const input = document.querySelector("input");
    const wall = document.querySelector(".wall");
    input.addEventListener('keypress', (event) => {
        if (event.code == "Enter") {
            const newValue = input.value.trim();
            wall.innerHTML = newValue;
            fetch('/api/wall?wall_text=' + newValue)
        }
    });
})