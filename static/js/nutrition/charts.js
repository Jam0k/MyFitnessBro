// Prepare data for the line chart
var dates = Object.keys(dailyMacrosData);
var macrosData = {
  Calories: dates.map((date) => dailyMacrosData[date].calories),
  "Total Fat": dates.map((date) => dailyMacrosData[date].total_fat),
  "Total Carbohydrate": dates.map(
    (date) => dailyMacrosData[date].total_carbohydrate
  ),
  "Total Sugars": dates.map((date) => dailyMacrosData[date].total_sugars),
  "Total Protein": dates.map((date) => dailyMacrosData[date].total_protein),
};

document.addEventListener("DOMContentLoaded", function () {
  var modalCtx = document
    .getElementById("modalMacroTrendsChart")
    .getContext("2d");
  var modalChart;

  $("#lineChartModal").on("show.bs.modal", function () {
    modalChart = new Chart(modalCtx, {
      type: "line",
      data: {
        labels: dates,
        datasets: Object.keys(macrosData).map((key) => {
          return {
            label: key,
            data: macrosData[key],
            // add additional styling as needed
          };
        }),
      },
      options: {
        // configure options as needed
      },
    });
  });

  $("#lineChartModal").on("hide.bs.modal", function () {
    modalChart.destroy();
  });
});
