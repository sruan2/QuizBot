function onLoad() {
    document.addEventListener("deviceready", onDeviceReady, false);
    console.log("on load")
}

function onDeviceReady() {
    console.log("on load")  
    console.log("app startup")
    document.addEventListener("pause", onPause, false);
    document.addEventListener("resume", onResume, false);
    cordova.plugins.notification.local.schedule({
        title: 'Reminder',
        text: 'Remember to do some flashcards today!',
        foreground: true,
        trigger: { every: { hour: 20, minute: 0 } }
    });
}

function onPause() {
    console.log("app pause")
}

function onResume() {
    console.log("app resume")
}

function log(message) {
    var json = {firstname: $user.firstname, lastname: $user.lastname, user_id: $user.id, qid: $question['qid'], event: message, timestamp: new Date().toISOString().slice(0, 19).replace('T', ' ')};
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
