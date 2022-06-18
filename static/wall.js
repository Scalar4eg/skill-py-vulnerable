window.addEventListener('load', (event) => {
    const input = document.querySelector("input");
    const wall = document.querySelector(".wall");
    input.addEventListener('keypress', (event) => {
        if (event.code == "Enter") {
            const newValue = input.value.trim();
            wall.innerHTML = newValue;
            if (newValue == "") {
                wall.classList.add('empty')
            } else {
                wall.classList.remove('empty')
            }
            const payload = new FormData(document.forms[0]);
            fetch("/api/wall", {method: 'POST', body: payload})
            event.preventDefault();
            return false;
        }
    });
})