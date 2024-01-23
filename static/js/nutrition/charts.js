  document.addEventListener('DOMContentLoaded', function() {
    {% if goal_data %}
      // Function to create a semi-circle progress bar
      var createSemiCircleProgressBar = function(containerId, currentValue, totalValue, color) {
        var progressBar = new ProgressBar.SemiCircle(containerId, {
          strokeWidth: 6,
          color: color,
          trailColor: '#eee',
          trailWidth: 1,
          easing: 'easeInOut',
          duration: 1400,
          svgStyle: null,
          text: {
            value: '',
            alignToBottom: false
          },
          from: { color: '#FFEA82' },
          to: { color: '#ED6A5A' },
          step: (state, bar) => {
            bar.setText(Math.round(bar.value() * totalValue) + ' / ' + totalValue);
            bar.path.setAttribute('stroke', state.color);
          }
        });

        progressBar.text.style.fontFamily = '"Helvetica Neue", Helvetica, Arial, sans-serif';
        progressBar.text.style.fontSize = '2rem';

        progressBar.animate(currentValue / totalValue);
      };

      // Initialize progress bars for each nutrient
      createSemiCircleProgressBar('#calories-container', {{ grand_total['calories'] }}, {{ goal_data.calories }}, 'blue');
      createSemiCircleProgressBar('#fat-container', {{ grand_total['total_fat'] }}, {{ goal_data.fat }}, 'green');
      createSemiCircleProgressBar('#carbs-container', {{ grand_total['total_carbohydrate'] }}, {{ goal_data.carbohydrates }}, 'orange');
      createSemiCircleProgressBar('#sugars-container', {{ grand_total['total_sugars'] }}, {{ goal_data.sugars }}, 'purple');
      createSemiCircleProgressBar('#protein-container', {{ grand_total['total_protein'] }}, {{ goal_data.protein }}, 'red');
    {% endif %}
  });