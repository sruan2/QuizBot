$('document').ready(
    function() {
        $('.element-front').show();
        $('.element-back').hide();
        $index = 0;
        update();
    }
);

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
    $index = $index < $questions.length - 1 ? $index + 1 : 0;
    update();
}

function prev() {
    $index = $index > 0 ? $index - 1 : $questions.length - 1;
    update();
}

function update() {
    // $questions are imported from questions.js
    $('#front').html("Q: " + $questions[$index].question);
    $('#back').html("A: " + $questions[$index].correct_answer[0]);
    $('#explanation').html($questions[$index].support);

    $choices = shuffle($questions[$index].distractor.concat($questions[$index].correct_answer));
    $hints = "<p>The answer is one of the following:</p><ol>"
    for ($c in $choices) {
        $hints += "<li>" + $choices[$c] + "</li>"
    }
    $('#hint').html($hints + "</ol>");

    $('#qid').html("Question " + parseInt($index + 1));
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
