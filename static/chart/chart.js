function drawLineChart(labels, data) {
    let ctx = document.getElementById('line-graph-canvas').getContext('2d');
    let chart = new Chart(ctx, {
        // 作成するグラフの種類
        type: 'line',

        // ラベルとデータセットを設定
        data: {
            labels: labels,
            datasets: [{
                label: "FX chart",
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: data,
            }]
        },

        // オプション設定
        options: {}
    });
};


$(function(){
    $('#update-btn').on('click', function(){
//        let input_data = $('#line-graph-form').serializeArray();
//        let input_data_dict = {}
//        $.each(input_data, function(i, val){
//            input_data_dict[val['name']] = val['value'];
//        });

        $.ajax('get_selected_fx_data/',{
            type: 'get',
//            data: input_data_dict
        }).done(function(data){
            console.log('success');
            let data_obj = JSON.parse(data);
//            drawLineChart(data_obj.time, data_obj.price);
            drawLineChart(['a', 'b', 'c'], [1, 2, 3]);
        }).fail(function(){
            console.log('fail');
        });
    });
});
