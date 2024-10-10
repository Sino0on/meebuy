document.addEventListener("DOMContentLoaded", function () {
    const options = document.querySelectorAll(".tarif-options");

    options.forEach((option) => {
        const radios = option.querySelectorAll('input[type="radio"]');
        const pricePerMonthElement = option.querySelector(".tarif-price strong");
        const totalAmountElement = option.querySelector(".tarif-total-amount strong");
        const periodElement = option.querySelector(".tarif-selected-period strong");

        radios.forEach((radio) => {
            radio.addEventListener("change", function () {
                const pricePerMonth = parseInt(this.dataset.price);
                const monthAmount = parseInt(this.dataset.monthAmount);
                const totalAmount = pricePerMonth * monthAmount;
                // Update the displayed price, period, and total
                pricePerMonthElement.textContent = `${pricePerMonth} сом`;
                periodElement.textContent = `${monthAmount} мес.`;
                totalAmountElement.textContent = `${totalAmount} сом`;
            });
        });

        radios.forEach((radio) => {
            if (radio.checked) {
                const pricePerMonth = parseInt(radio.dataset.price);
                const monthAmount = parseInt(radio.dataset.monthAmount);
                const totalAmount = pricePerMonth * monthAmount;
                // Update the displayed price, period, and total
                pricePerMonthElement.textContent = `${pricePerMonth} сом`;
                periodElement.textContent = `${monthAmount} мес.`;
                totalAmountElement.textContent = `${totalAmount} сом`;
            }
        });
    });
});
