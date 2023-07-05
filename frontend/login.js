const form = document.querySelector("#form-login");

form.addEventListener("submit", handleSubmitLoginForm);

async function handleSubmitLoginForm(event) {
  event.preventDefault();

  const warnning = document.querySelector("#info-login");
  warnning.style.color = "red";

  const body = new FormData(form);
  body.set("password", sha256(body.get("password")));

  const res = await fetch("/login", {
    method: "POST",
    body: body,
  });
  const data = await res.json();

  if (res.status === 200) {
    warnning.textContent = null;
    window.localStorage.setItem("access token", `${data.access_token}`);
    window.location.pathname = "/";
  } else if (res.tatus === 401) {
    warnning.textContent = "아이디 혹은 비밀번호가 옳지 않습니다.";
  } else {
    warnning.textContent = "로그인에 실패했습니다.";
  }
}
