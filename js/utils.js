
function decodeHidden(event, mailStringBase64) {
    event.preventDefault();
    let elem = event.target;
    let domain = "proton.me";
    let repeatCount = 100;
    let mailString = atob(mailStringBase64);

    function finalize() {
        elem.href = 'mailto:' + mailString;
        elem.innerHTML = mailString;
        elem.removeAttribute("onclick");
        console.log(event.target);
    }

    times = 0;
    requestAnimationFrame(function action(time) {
        let x = (Math.random() + 1).toString(36).substring(2);
        elem.innerHTML = x + domain;

        if (times++ < repeatCount) { requestAnimationFrame(action) }
        else { finalize(); }
    })
}
