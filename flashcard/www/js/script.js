$('document').ready(
    function() {
        $('#front').show();
        $('#back').hide();
        $index = 0;
        update();
    }
);

function flip() {
    if ($('#front').is(":visible")) {
        $('#front').hide();
        $('#back').show();
    } else {
        $('#front').show();
        $('#back').hide();
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
    $('#front').html($questions[$index].question);
    $('#back').html($questions[$index].correct_answer[0]);
}
