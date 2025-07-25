var user_id;

$('document').ready(
    function() {
        $subject = 'science';
        $qid = null;
        load();
        fetch_question();
        FastClick.attach(document.body);
        $('.element-front').show();
        $('.element-back').hide();

        // remove focus of the button.
        $(".btn").click(function(event) {
            $(this).blur();
        });
    }
)

function change(subject) {
    $subject = subject;
    fetch_question();
    if (!$('#front').is(":visible")) {
        flip();
    }
    log('change to ' + subject, $question["qid"][1])
}


function flip() {
    if ($('#front').is(":visible")) {
        $('.element-front').hide();
        $('.element-back').show();
        log("card flip to answer", $question["qid"][1]);
    } else {
        $('.element-back').hide();
        $('.element-front').show();
        log("card flip to question", $question["qid"][1]);
    }
}


function flip_to_front() {
    if (!$('#front').is(":visible")) {
        $('.element-back').hide();
        $('.element-front').show();
        log("card flip to question", $question["qid"][1]);
    }
}


function got_it() {
    fetch_question();
    flip_to_front()
    log("got it", $question["qid"][1]);
}


function not_got_it() {
    fetch_question();
    flip_to_front()
    log("I don't know", $question["qid"][1]);
}


function update(question) {
    console.log('update:' + question['qid'][1]);
    console.log(question)
    $('#front').html("Q: " + question['question']);
    $('#back').html("A: " + question['correct_answer']);
    $('#explanation').html(question['support']);

    $choices = shuffle(question['distractor'].concat(question['correct_answer']));
    $hints = "<p>The answer is one of the following:</p><ol>"
    for ($c in $choices) {
        $hints += "<li>" + $choices[$c] + "</li>"
    }
    $('#hint').html($hints + "</ol>");

    $('#qid').html("Question " + question['qid'][1]);
}


function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}


function load() {
    if (!window.localStorage.getItem('user')) {
        $('#userModal').modal();
        $('#firstname').val('');
        $('#lastname').val('');
    } else {
        $user = JSON.parse(window.localStorage.getItem('user'));
        $('#userLabel').html($user.firstname + ' ' + $user.lastname);
        $('#firstname').val($user.firstname);
        $('#lastname').val($user.firstname + ' ' + $user.lastname);
    }
    console.log('load: ' + $user);
    user_id = $user.id;
}


function fetch_question() {
    if ($subject === "science" ) {
        fetch('/question_data_science?user_id=' + user_id).then(function(response) {
            response.json().then(function(json) {
                $question = json;
                update($question);
            });
        });
    }
    else if ($subject === "safety" ) {
        fetch('/question_data_safety?user_id=' + user_id).then(function(response) {
            response.json().then(function(json) {
                $question = json;
                update($question);
            });
        });
    }
    else if ($subject === "gre" ) {
        fetch('/question_data_gre?user_id=' + user_id).then(function(response) {
            response.json().then(function(json) {
                $question = json;
                update($question);
            });
        });
    }
    else {
        fetch('/question_data?user_id=' + user_id).then(function(response) {
            response.json().then(function(json) {
                $question = json;
                update($question);
            });
        });
    }
}


function save() {
    var firstname = $('#firstname').val();
    var lastname = $('#lastname').val();
    var uid = encode(firstname + lastname);
    $user = {firstname: firstname, lastname: lastname, id: uid};
    $('#userLabel').html($user.firstname + ' ' + $user.lastname);
    window.localStorage.setItem('user', JSON.stringify($user));
}


function hint() {
    log('toggle hint', $question["qid"][1]);
}

function explanation() {
    log('toggle explanation', $question["qid"][1]);
}


function encode(str) {
	var hash = 0;
	if (str.length == 0) {
        return hash;
    }
	for (i = 0; i < str.length; i++) {
		char = str.charCodeAt(i);
		hash = ((hash<<5)-hash)+char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return Math.abs(hash);
}
