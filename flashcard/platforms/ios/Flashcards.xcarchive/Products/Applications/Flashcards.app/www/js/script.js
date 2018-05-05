$('document').ready(
    function() {
        $user = 'brycetham'
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
        change('science');
    }
);

function change(subject) {
    $subject = subject;
    if (!$('#front').is(":visible")) {
        flip();
    }
    $.ajax({
        url: 'https://www.smartprimer.org:5000/test',
        type: 'GET',
        data: {
            user: $user,
            timestamp: new Date(),
            subject: $subject,
        },
        complete: function(data) {
            console.log({user: $user, timestamp: new Date().toString(), subject: $subject});
        }
    });
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
};

function next() {
    $index[$subject] = $index[$subject] < $data[$subject].length - 1 ? $index[$subject] + 1 : 0;
    if (!$('#front').is(":visible")) {
        flip();
    }
    update();
}

function prev() {
    $index[$subject] = $index[$subject] > 0 ? $index[$subject] - 1 : $data[$subject].length - 1;
    if (!$('#front').is(":visible")) {
        flip();
    }
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
