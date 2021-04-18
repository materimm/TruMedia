$(function () {
  //activate tooltips on page load
  $('[data-toggle="tooltip"]').tooltip();

  //replace escaped quotes and parse to json
  obj = obj.replaceAll('&#39;', "\"");
  obj = JSON.parse(obj);

  let cmpp = build_line_chart('cmp', obj.labels, obj.cmpp_per_game, 'CMP%', obj.team_color, 'Completion Percentage Each Week', obj.oppImgs);
  let ypa = build_line_chart('ypa', obj.labels, obj.ypa_per_game, 'Yd/Att', obj.team_color, 'Yards Per Attempt Each Week', obj.oppImgs);
});

//function to create a line chart using the ChartJS library
function build_line_chart(id, labels, data, dataLabel, color, title, imgs) {
  var ctx = document.getElementById(id).getContext('2d');
  var line_chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: dataLabel,
            data: data,
            backgroundColor: color,
            borderColor: color,
            fill: false,
            borderWidth: 3
        }]
    },
    plugins: {
      //replace points with logo imgs
      afterUpdate: chart => {
        if(imgs != null) {
          let points = chart.getDatasetMeta(0).data;
          for(let i=0; i<points.length; i++) {
            let img = new Image();
            img.src = imgs[i];
            img.width = 30;
            img.height = 30;
            points[i]._model.pointStyle = img;
          }
        }
      }
    },
    options: {
        title: {
          display: true,
          text: [title,
                "Season: 2018"]
        },
        maintainAspectRatio: false
    }
  });
}
