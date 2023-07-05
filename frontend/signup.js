const form = document.querySelector("#form-signup");

form.addEventListener("submit", handleSubmitForm);

async function handleSubmitForm(event) {
  event.preventDefault();
  const body = new FormData(form);
  const warnning = document.querySelector("#info");
  warnning.style.color = "red";

  if (body.get("password") === body.get("password2")) {
    body.set("password", sha256(body.get("password")));
    const res = await fetch("/signup", {
      method: "POST",
      body: body,
    });
    const data = await res.json();
    if (data === "200") {
      warnning.textContent = null;
      window.location.pathname = "/login.html";
    } else if (data === "401")
      warnning.textContent = "이미 존재하는 아이디입니다.";
    else warnning.textContent = "회원가입에 실패했습니다.";
  } else warnning.textContent = "비밀번호가 서로 맞지 않습니다!";
}
