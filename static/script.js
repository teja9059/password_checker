function checkPassword() {
    let pwd = document.getElementById("password").value;

    fetch("/check", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "password=" + pwd
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("entropy").innerText = "Entropy: " + data.entropy;
        document.getElementById("suggestion").innerText = data.suggestion;

        let l1 = document.getElementById("light1");
        let l2 = document.getElementById("light2");
        let l3 = document.getElementById("light3");

        // Reset
        l1.style.background = "gray";
        l2.style.background = "gray";
        l3.style.background = "gray";

        if (data.score <= 2) {
            l1.style.background = "red";
            document.getElementById("strength").innerText = "Weak ❌";
        } 
        else if (data.score <= 4) {
            l1.style.background = "orange";
            l2.style.background = "orange";
            document.getElementById("strength").innerText = "Medium ⚠️";
        } 
        else {
            l1.style.background = "green";
            l2.style.background = "green";
            l3.style.background = "green";
            document.getElementById("strength").innerText = "Strong ✅";
        }
    });
}
function togglePassword() {
    let pwd = document.getElementById("password");
    let eye = document.getElementById("eye");

    if (pwd.type === "password") {
        pwd.type = "text";
        eye.innerText = "🙈";
    } else {
        pwd.type = "password";
        eye.innerText = "👁️";
    }
}