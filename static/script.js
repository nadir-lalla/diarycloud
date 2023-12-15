const date = new Date();
const day = date.getDate();
const month = date.toLocaleString("default", { month: "short" });
const year = date.getFullYear();
const formattedDate = `${day} ${month} ${year}`;

document.getElementById("entry").placeholder = `Make an entry for today, ${formattedDate}`;
