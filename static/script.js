document.getElementById("search").addEventListener("click", function(event) {
    event.preventDefault();
    let value = document.getElementById('search_place').value;
    if (value !== '') {
        let progress = document.getElementById("progress");
        progress.classList.add('bg-info');
        progress.classList.add('progress-bar-striped');
        progress.classList.add('progress-bar-animated');
        let token = new FormData();
        token.append('search', value);
        fetch('/stop', {
                method: 'POST',
                credentials: 'same-origin',
                body: token,
            }).then(response => response.text())
            .then(tables => $("body").html(tables))
            .catch(function(err) {
                console.log(err);
            });
    }
});


document.getElementById("refresh").addEventListener("click", function(event) {
    event.preventDefault();
    let token = new FormData();
    let stop_id = document.getElementById('stop_id').innerHTML;
    if (stop_id !== 'Wybierz przystanek...') {
        token.append('search', stop_id);
        fetch('/stop', {
                method: 'POST',
                credentials: 'same-origin',
                body: token,
            }).then(response => response.text())
            .then(tables => $("body").html(tables))
            .catch(function(err) {
                console.log(err);
            });
    }
});