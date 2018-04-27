$('document').ready(
    function() {
        $('.element-front').show();
        $('.element-back').hide();
        $('#hint').hide();
        $('#explanation').hide();
        $index = 0;
        update();
    }
);

function flip() {
    if ($('#front').is(":visible")) {
        $('.element-front').hide();
        $('.element-back').show();
        $('#hint').hide();
    } else {
        $('.element-front').show();
        $('.element-back').hide();
        $('#explanation').hide();
    }
};

function hint() {
    if ($('#hint').is(":visible")) {
        $('#front').show();
        $('#hint').hide();
    } else {
        $('#front').hide();
        $('#hint').show();
    }
}

function explanation() {
    if ($('#explanation').is(":visible")) {
        $('#back').show();
        $('#explanation').hide();
    } else {
        $('#back').hide();
        $('#explanation').show();
    }
}

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
    $('#explanation').html("Explanation: " + $questions[$index].support);

    $choices = shuffle($questions[$index].distractor.concat($questions[$index].correct_answer));
    $hints = ""
    for ($c in $choices) {
        $hints += (parseInt($c)+1) + ". " + $choices[$c] + "<br />"
    }
    $('#hint').html($hints);

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
