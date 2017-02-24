
function GetColours() {
    var array = [
        document.getElementById("red").value,
        document.getElementById("green").value,
        document.getElementById("blue").value
    ];

    //array = [for (i of array) parseInt(i)];

    for (i = 0; i < array.length; i++) {
        colour = parseInt(array[i]);
        if (!Number.isInteger(colour) || colour < 0 || colour > 255) {
            array[i] = 0;
        } else {
            array[i] = colour;
        }
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/colours", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
        JSON.stringify(
            {
                "red": array[0],
                "green": array[1],
                "blue": array[2]
            }
        )
    );

    document.body.style.backgroundColor = `rgb(${red_colour}, ${green_colour}, ${blue_colour})`;
}
