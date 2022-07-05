/* 
  Execute when the page finishes loading
  Gets the Django error elements and puts them inside a <div> (class="errorlist")
  Also makes the success <div> appears if theres any <ul> inside
*/
(function () {
    screen.orientation.lock("portrait");

    // Get the messages <ul>
    var messages = document.querySelector(".messages");

    // Get the errors <ul>
    var errorlists = document.querySelectorAll(".errorlist");

    if (messages != undefined) {
        // Insert every error <li> from each errorlist <ul> into the messages <ul>
        errorlists.forEach((errorlist) => {
            errors = errorlist.querySelectorAll("li");
            errors.forEach((error) => {
                error.classList.add("error");
                messages.insertAdjacentElement("afterbegin", error);
            });
        });

        messages.addEventListener("animationend", function () {
            setTimeout(function () {
                messages.remove();
            }, 0);
        });
    }

    preventIncognito();
})();

function preventIncognito() {
    detectIncognito().then((result) => {
        if (result.isPrivate) {
            document
                .querySelectorAll("button[type='submit']")
                .forEach((button) => {
                    button.classList.add("disabled");
                    button.disabled = true;
                    button.parentElement.classList.add("disabled");
                    button.parentElement.addEventListener(
                        "click",
                        alertIncognito,
                        false
                    );
                });
            document
                .querySelectorAll("input[name='csrfmiddlewaretoken']")
                .forEach((input) => {
                    input.remove();
                });
        }
    });
}

function alertIncognito() {
    alert(
        gettext(
            "Não é permitido realizar esta ação com o navegador em modo anônimo."
        )
    );
}

var onloadCallback = function () {
    preventIncognito();
};
