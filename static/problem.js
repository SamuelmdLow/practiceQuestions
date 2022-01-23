function checkAnswer(answer)
{
    guess = document.getElementById("answer");
    if (guess == answer)
    {
        alert("Correct!");
    }
    else
    {
        alert("Wrong");
    }
}