const form = document.querySelector("#form-write");
form.addEventListener("submit", handleSubmitForm);

async function handleSubmitForm(event) {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());

  const res = await fetch("/items", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem("access token")}`,
    },
    body: body,
  });
  const data = await res.json();
  if (data === "200") {
    window.location.pathname = "/";
  } else console.log("글쓰기에 실패했습니다.");
}
