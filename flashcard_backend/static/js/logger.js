function onLoad() {
    document.addEventListener("deviceready", onDeviceReady, false);
}

function onDeviceReady() {
    log("app startup");
    document.addEventListener("pause", onPause, false);
    document.addEventListener("resume", onResume, false);
    cordova.plugins.notification.local.schedule({
        text: "Remember to do some flashcards if you haven't finished your session today!",
        trigger: { every: { hour: 20, minute: 0 } }
    });
    log("send reminder");
}

function onPause() {
    log("app pause");
}

function onResume() {
    log("app resume");
}

function log(message, input_qid) {
    console.log('qid:' + input_qid)
    var json = {firstname: $user.firstname, lastname: $user.lastname, user_id: $user.id, qid: input_qid, event: message, timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')};
    $.ajax({
        url: 'https://www.smartprimer.org:5000/logdata',
        // url:'https://localhost:5000/logdata',
        type: 'POST',
        contentType: 'text/plain',
        data: JSON.stringify(json),
        complete: function() {
            console.log('Logged: ' + JSON.stringify(json));
        }
    });
}
