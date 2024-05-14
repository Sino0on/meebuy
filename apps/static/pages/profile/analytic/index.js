const statistics = document.getElementById("statistics");
const lifting = document.getElementById("lifting");
const bannery = document.getElementById("bannery");
const verification = document.getElementById("verification");
const rates = document.getElementById("rates");
const goodsBlock = document.getElementById("statistics-block");
const categoryBlock = document.getElementById("lifting-block");
const priceBlock = document.getElementById("bannery-block");
const autoloaderBlock = document.getElementById("verification-block");
const excelLoaderBlock = document.getElementById("rates-block");

const toggleTab = (element) => {
  const tabs = [statistics, lifting, bannery, verification, rates];
  const blocks = [
    goodsBlock,
    categoryBlock,
    priceBlock,
    autoloaderBlock,
    excelLoaderBlock,
  ];
  for (let i = 0; i <= tabs.length; i++) {
    if (tabs[i] === element) {
      tabs[i].style.backgroundColor = "#FFFB98";
      blocks[i].style.display = "block";
    } else {
      tabs[i].style.backgroundColor = "";
      blocks[i].style.display = "none";
    }
  }
};

statistics.addEventListener("click", () => toggleTab(statistics));
lifting.addEventListener("click", () => toggleTab(lifting));
bannery.addEventListener("click", () => toggleTab(bannery));
verification.addEventListener("click", () => toggleTab(verification));
rates.addEventListener("click", () => toggleTab(rates));

// chart

const ctx = document.getElementById("myChart");
if (window.innerWidth < 430) {
  ctx.width = 370;
  ctx.height = 180;
} else {
  ctx.width = 660;
  ctx.height = 200;
}

const data = [
  {
    x: "Сегодня",
    net: 10000,
    cogs: 550,
    gm: 7500,
    netFourth: 5040,
    cogsFifth: 9000,
  },
  {
    x: "Вчера",
    net: 100,
    cogs: 5150,
    gm: 2150,
    netFourth: 5040,
    cogsFifth: 5000,
  },
  {
    x: "Месяц",
    net: 1500,
    cogs: 5670,
    gm: 1650,
    netFourth: 3040,
    cogsFifth: 6000,
  },
  {
    x: "Год",
    nnet: 7150,
    cogs: 6750,
    gm: 1500,
    netFourth: 5040,
    cogsFifth: 4000,
  },
];
new Chart(ctx, {
  type: "bar",
  data: {
    labels: data.map((entry) => entry.x),
    datasets: [
      {
        label: "",
        data: data,
        backgroundColor: "#0407A3",
        parsing: {
          yAxisKey: "net",
        },
      },
      {
        label: "",
        data: data,
        backgroundColor: "#6713F6",
        parsing: {
          yAxisKey: "cogs",
        },
      },
      {
        label: "",
        data: data,
        backgroundColor: "#DDD7E4",
        parsing: {
          yAxisKey: "gm",
        },
      },
      {
        label: "",
        data: data,
        backgroundColor: "#7E8BE2",
        parsing: {
          yAxisKey: "netFourth",
        },
      },
      {
        label: "",
        data: data,
        backgroundColor: "#5EB7F2",
        parsing: {
          yAxisKey: "cogsFifth",
        },
      },
    ],
  },
  options: {
    scales: {
      y: {
        min: 0,
        ticks: {
          stepSize: 1000,
        },
      },
    },
  },
});
