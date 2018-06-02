function onLoad() {
    document.addEventListener("deviceready", onDeviceReady, false);
}

function onDeviceReady() {
    log("app startup");
    document.addEventListener("pause", onPause, false);
    document.addEventListener("resume", onResume, false);
    cordova.plugins.notification.local.schedule({
        text: 'Remember to do some flashcards today!',
        trigger: { every: { hour: 20, minute: 0 } }
    });
}

function onPause() {
    log("app pause");
}

function onResume() {
    log("app resume");
}

function log(message) {
    $.ajax({
        url: 'https://www.smartprimer.org:5000/logdata',
        type: 'POST',
        data: {
            data: {
                firstname: $user.firstname,
                lastname: $user.lastname,
                user_id: $user.id,
                qid: $question.id,
                event: message
            }
        },
        complete: function(data) {
            console.log({firstname: $user.firstname, lastname: $user.lastname, user_id: $user.id, qid: $question.id, event: message});
        }
    });
}
