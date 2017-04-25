
function GetColors() {
    let array = [
        document.getElementById("red").value,
        document.getElementById("green").value,
        document.getElementById("blue").value
    ];

    array = array.map(i => parseInt(i));

    for (let i = 0; i < array.length; i++) {
        if (!Number.isInteger(array[i]) || array[i] < 0 || array[i] > 255) {
            array[i] = 0;
        }
    }

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/colors", true);
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

    document.body.style.backgroundColor = `rgb(${array[0]}, ${array[1]}, ${array[2]})`;
}
/*
Compile the file script.js and output to stdout.
babel script.js
# output...

If you would like to output to a file you may use --out-file or -o.
babel script.js --out-file script-compiled.js

To compile a file every time that you change it, use the --watch or -w option:
babel script.js --watch --out-file script-compiled.js
*/