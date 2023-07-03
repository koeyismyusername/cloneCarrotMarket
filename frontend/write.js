const form = document.querySelector("#form-write");
form.addEventListener("submit", handleSubmitForm);

async function handleSubmitForm(event) {
  event.preventDefault();
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime());

  await fetch("/items", {
    method: "POST",
    body: body,
  });
}
