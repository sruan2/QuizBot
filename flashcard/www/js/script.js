$('document').ready(
    function() {
        $('#front').show();
        $('#back').hide();
        $index = 0
        $json = {
            "questions": [
                {"front": "QuizBot", "back": "a chatbot for learning"},
                {"front": "Apotheosis", "back": "a model of excellence"},
                {"front": "Consummate", "back": "having supreme mastery"},
                {"front": "Debonair", "back": "having a sophisticated charm"},
                {"front": "Expansive", "back": "friendly and open"},
                {"front": "Intransigent", "back": "impervious to persuasion"},
                {"front": "Stolid", "back": "having little emotion"},
                {"front": "Vicissitude", "back": "variation in circumstance"}
            ]
        }
        $('#front').html($json.questions[$index].front);
        $('#back').html($json.questions[$index].back);
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
    $index = $index < $json.questions.length - 1 ? $index + 1 : 0;
    $('#front').html($json.questions[$index].front);
    $('#back').html($json.questions[$index].back);
}

function prev() {
    $index = $index > 0 ? $index - 1 : $json.questions.length - 1;
    $('#front').html($json.questions[$index].front);
    $('#back').html($json.questions[$index].back);
}
