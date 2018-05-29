$('document').ready(
    function() {
        load();
        FastClick.attach(document.body);
        $('.element-front').show();
        $('.element-back').hide();
        $data = {
            science: [],
            gre: [],
            safety: [],
        };
        for ($q in $questions) {
            if ($questions[$q].subject === 'gre') {
                $data['gre'].push($questions[$q]);
            } else if ($questions[$q].subject === 'safety') {
                $data['safety'].push($questions[$q]);
            } else {
                $data['science'].push($questions[$q]);
            }
        }
        for ($d in $data) {
            shuffle($data[$d]);
        }
        $index = {
            science: 0,
            gre: 0,
            safety: 0,
        };
        $subject = 'science';
        update();
    }
);

function change(subject) {
    $subject = subject;
    if (!$('#front').is(":visible")) {
        flip();
    }
    log('change to ' + subject)
    update();
}

function flip() {
    if ($('#front').is(":visible")) {
        $('.element-front').hide();
        $('.element-back').show();
    } else {
        $('.element-front').show();
        $('.element-back').hide();
    }
    log("card flip");
};

function next() {
    $index[$subject] = $index[$subject] < $data[$subject].length - 1 ? $index[$subject] + 1 : 0;
    if (!$('#front').is(":visible")) {
        flip();
    }
    log("card next");
    update();
}

function prev() {
    $index[$subject] = $index[$subject] > 0 ? $index[$subject] - 1 : $data[$subject].length - 1;
    if (!$('#front').is(":visible")) {
        flip();
    }
    log("card prev");
    update();
}

function update() {
    // $questions are imported from questions.js
    $question = $data[$subject][$index[$subject]];
    $('#front').html("Q: " + $question.question);
    $('#back').html("A: " + $question.correct_answer[0]);
    $('#explanation').html($question.support);

    $choices = shuffle($question.distractor.concat($question.correct_answer));
    $hints = "<p>The answer is one of the following:</p><ol>"
    for ($c in $choices) {
        $hints += "<li>" + $choices[$c] + "</li>"
    }
    $('#hint').html($hints + "</ol>");

    $('#qid').html("Question " + parseInt($index[$subject] + 1));
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
        $('#lastname').val($user.lastname);
    }
}

function save() {
    $user = {firstname: $('#firstname').val(), lastname: $('#lastname').val()};
    $('#userLabel').html($user.firstname + ' ' + $user.lastname);
    window.localStorage.setItem('user', JSON.stringify($user));
}

function hint() {
    log('toggle hint');
}

function explanation() {
    log('toggle explanation');
}
