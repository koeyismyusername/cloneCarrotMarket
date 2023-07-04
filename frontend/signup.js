const form = document.querySelector("#form-signup");

form.addEventListener("submit", handleSubmitForm);

async function handleSubmitForm(event) {
  event.preventDefault();
  const body = new FormData(form);

  if (body.get("password") === body.get("password2")) {
    body.set("password", sha256(body.get("password")));
    const res = await fetch("/signup", {
      method: "POST",
      body: body,
    });
    window.location.pathname = "/";
  } else {
    const warnning = document.querySelector("#info");
    warnning.textContent = "비밀번호가 서로 맞지 않습니다!";
    warnning.style.color = "red";
  }
}
