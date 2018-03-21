function drawLineChart(dom_id, labels, data) {
    let ctx = document.getElementById(dom_id).getContext('2d');
    // 描写済みの場合は削除
    // TODO 挙動変
    if (typeof chart !== "undefined") {
//        chart.destroy();
    }
    let pointBgColor = generatePointBgColor(data.position);
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
                pointRadius: 4,
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: data.rate,
                // マーカーの背景色
                pointBackgroundColor: pointBgColor,
            },{
                label: "technical index",
                //面の表示
                fill: false,
                //線のカーブ
                lineTension: 0,
                //接合点のサイズ
                pointRadius: 1,
                backgroundColor: 'rgba(1, 99, 132, 0.3)',
                borderColor: 'rgba(1, 99, 132, 0.3)',
                data: data.technical_index,
            }]
        },

        // オプション設定
        options: {}
    });
};

/**
 * position変化によるマーカ背景色コントロール配列の作成
 * @param position: position情報を持つ配列
*/
function generatePointBgColor(position) {

    let bgColor = [];

    colorDict= {
        longOpen: 'rgba(255, 127, 127, 1.0)',
        longClose: 'rgba(255, 127, 191, 1.0)',
        shortOpen: 'rgba(127, 191, 255, 1.0)',
        shortClose: 'rgba(127, 255, 255, 1.0)',
        normal: 'rgba(153, 153, 153, 1.0)',
    }

    for(var i=0, len=position.length; i<len; i++ ) {

        switch (position[i]) {
            case 1:
                bgColor.push(colorDict.longOpen);
                break;

            case 2:
                bgColor.push(colorDict.longClose);
                break;

            case 3:
                bgColor.push(colorDict.shortOpen);
                break;

            case 4:
                bgColor.push(colorDict.shortClose);
                break;

            case 0:
                bgColor.push(colorDict.normal);
                break;
        }

    }
    return bgColor

}


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
            let att_data = {'time': data_obj.time, 'asset': data_obj.asset_transition,'rate': data_obj.rate,
                            'position': data_obj.position, 'technical_index':data_obj.technical_index}
            drawLineChart('line-graph-canvas1', data_obj.time, att_data);
        }).fail(function(){
            console.log('fail');
        });
    });
});