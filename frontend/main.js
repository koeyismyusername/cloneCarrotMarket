const wrapper = document.querySelector("main > .wrapper");

fetchItemList();

async function fetchItemList() {
  const res = await fetch("/items", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${window.localStorage.getItem("access token")}`,
    },
  });
  const items = await res.json();
  renderItemList(items);
}

function renderItemList(items) {
  items.forEach(async (item) => {
    const content = document.createElement("div");
    wrapper.appendChild(content);
    content.classList.add("content");
    const res = await fetch(`/images/${item.id}`);
    const imgBlob = await res.blob();
    const imgURL = URL.createObjectURL(imgBlob);
    content.innerHTML = `<img
    class="image"
    src="${imgURL}"
    alt="이미지를 불러올 수 없습니다"
  />
  <div class="text-group">
    <div class="title">${item.title}</div>
    <div class="meta">
      <span class="location">${item.place}</span>
      <span> · </span>
      <span class="time">${getTimeStamp(item.insertAt)}</span>
    </div>
    <div class="price">${item.price.toLocaleString("ko-KR")}원</div>
  </div>`;
  });
}

function getTimeStamp(insertAt) {
  const timeDif = new Date(new Date().getTime() - insertAt);
  if (timeDif.getUTCFullYear() - 1970 > 0)
    return `${timeDif.getUTCFullYear() - 1970}년 전`;
  if (timeDif.getUTCMonth() > 0) return `${timeDif.getUTCMonth()}개월 전`;
  if (timeDif.getUTCDate() - 1 > 0) return `${timeDif.getUTCDate() - 1}일 전`;
  if (timeDif.getUTCHours() > 0) return `${timeDif.getUTCHours()}시간 전`;
  if (timeDif.getUTCMinutes() > 0) return `${timeDif.getUTCMinutes()}분 전`;
  if (timeDif.getUTCSeconds() > 0) return `${timeDif.getUTCSeconds()}초 전`;
  return "방금 전";
}
