
function GetColours() {
    var red_colour = document.getElementById("red").value;
    var green_colour = document.getElementById("green").value;
    var blue_colour = document.getElementById("blue").value;

    red_colour = parseInt(red_colour);
    green_colour = parseInt(green_colour);
    blue_colour = parseInt(blue_colour);

    if (!Number.isInteger(red_colour) || 0 > red_colour || red_colour > 255) {
        red_colour = 0;
    }

    if (!Number.isInteger(green_colour) || 0 > green_colour || green_colour > 255) {
        green_colour = 0;
    }

    if (!Number.isInteger(blue_colour) || 0 > blue_colour || blue_colour > 255) {
        blue_colour = 0;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/colours", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
        JSON.stringify(
            {
                "red": red_colour,
                "green": green_colour,
                "blue": blue_colour
            }
        )
    );

    document.body.style.backgroundColor = `rgb(${red_colour}, ${green_colour}, ${blue_colour})`;
}
