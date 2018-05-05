function onLoad() {
    document.addEventListener("deviceready", onDeviceReady, false);
}

function onDeviceReady() {
    log("app startup");
    document.addEventListener("pause", onPause, false);
    document.addEventListener("resume", onResume, false);
}

function onPause() {
    log("app pause");
}

function onResume() {
    log("app resume");
}

function log(message) {
    $.ajax({
        url: 'https://www.smartprimer.org:5000/test',
        type: 'GET',
        data: {
            user: $user,
            timestamp: new Date(),
            message: message,
        },
        complete: function(data) {
            console.log({user: $user, timestamp: new Date().toString(), message: message});
        }
    });
}
