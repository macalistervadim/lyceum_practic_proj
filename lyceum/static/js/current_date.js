const copyrightElement = document.getElementById("current-year");

const currDate = new Date();
const dateDiff = Math.abs((serverDate - currDate) / (3600*1000));

if (dateDiff < 24) {
    copyrightElement.textContent = String(currDate.getFullYear());
}