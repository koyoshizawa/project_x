function drawLineChart(labels, data) {
    let ctx = document.getElementById('line-graph-canvas').getContext('2d');
    // 描写済みの場合は削除
    // TODO 挙動変
    if (typeof chart !== "undefined") {
//        chart.destroy();
    }
    chart = new Chart(ctx, {
        // 作成するグラフの種類
        type: 'line',

        // ラベルとデータセットを設定
        data: {
            labels: labels,
            datasets: [{
                label: "FX chart",
                //面の表示
                fill: false,
                //線のカーブ
                lineTension: 0,
                //接合点のサイズ
                pointRadius: 1,
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

    //gloabal変数の定義
    var chart;  // 2回目以降に前回作成chart削除を行うために、chartのインスタンスはglobal変数で保持

    $('#update-btn').on('click', function(){
        let input_data = $('#line-graph-form').serializeArray();
        let input_data_dict = {}
        $.each(input_data, function(i, val){
            input_data_dict[val['name']] = val['value'];
        });

        // 日付が入力されていることの確認
        if (input_data_dict.date_from === "" || input_data_dict.date_to === "" ) {
            alert('日付が入力されてない！')
            return
        }

        // date to > date from の確認
        let date_from = parseInt(input_data_dict.date_from.replace(/-/g, ""));
        let date_to = parseInt(input_data_dict.date_to.replace(/-/g, ""));
        if (date_to <= date_from) {
            alert('終了日<=開始日になってる！')
            return
        }


        $.ajax('exec_back_test/',{
            type: 'post',
            cache: false,
            data: input_data_dict
        }).done(function(data){
            let data_obj = JSON.parse(data);
            drawLineChart(data_obj.time, data_obj.asset_transition);
        }).fail(function(){
            console.log('fail');
        });
    });
});