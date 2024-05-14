const replenishment = document.getElementById("replenishment");
const historyPayment = document.getElementById("history-payment");

const replenishmentBlock = document.getElementById("replenishment-block");
const historyPaymentBlock = document.getElementById("history-payment-block");

const toggleTabBalance = (element) => {
  const tabs = [replenishment, historyPayment];
  const blocks = [replenishmentBlock, historyPaymentBlock];
  for (let i = 0; i <= tabs.length; i++) {
    if (tabs[i] === element) {
      tabs[i].style.backgroundColor = "#fffb98";
      blocks[i].style.display = "block";
    } else {
      tabs[i].style.backgroundColor = "";
      blocks[i].style.display = "none";
    }
  }
};

replenishment.addEventListener("click", () => toggleTabBalance(replenishment));
historyPayment.addEventListener("click", () =>
  toggleTabBalance(historyPayment)
);

// open confirm tarif modal
const mbank = document.getElementById("mbank");
const odengi = document.getElementById("o-dengi");
const balance = document.getElementById("balance");
const pay24 = document.getElementById("pay24");
const openModal = document.getElementById("open-modal");

const buttons = document.getElementById("buttons");

const connectTarifButton = document.getElementById("connect-tarif-button");
const closeModal = document.getElementById("close_confirm");

const toggleConfirmModal = () => {
  openModal.style.display =
    openModal.style.display === "none" ? "block" : "none";
};
const toggleCloseConfirmModal = () => {
  openModal.style.display = "none";
};
const toggleConnectTarif = () => {
  buttons.style.display = "none";
};

mbank.addEventListener("click", toggleConfirmModal);
odengi.addEventListener("click", toggleConfirmModal);
balance.addEventListener("click", toggleConfirmModal);
pay24.addEventListener("click", toggleConfirmModal);
connectTarifButton.addEventListener("click", toggleConnectTarif);
closeModal.addEventListener("click", toggleCloseConfirmModal);
