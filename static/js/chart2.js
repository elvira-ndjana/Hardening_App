$(document).ready(function (){
    $.get("../informations2/",{},function(data){
        var ctx = document.getElementById('lineChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mars', 'Avr', 'Mai', 'Juin', 'Jul', 'Août', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Nombre d opérations',
                    data: [data.m01, data.m02, data.m03, data.m04, data.m05, data.m06, data.m07,
                     data.m08, data.m09, data.m10, data.m11, data.m12],
                    backgroundColor: [
                        'rgba(248, 134, 34,1)'

                    ],
                    borderColor: 'rgba(248, 134, 34, 1)',

                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    });


    $.get("../informations1/",{},function(data1){
        $(".durcissement").text(data1.durcissement)
        $(".verifications").text(data1.verifications)
        $(".autres").text(data1.autres)
        $(".conformite").text(data1.conformite)
        var ctx = document.getElementById('doughnut').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Durcissement', 'Vérification', 'Ajout/Suppression de contrôles', 'Correction des non conformités'],

                datasets: [{
                    label: 'Employees',
                    data: [data1.durcissement, data1.verifications, data1.autres, data1.conformite],
                    backgroundColor: [
                        'rgba(248, 134, 34,1)',
                        'rgba(0, 0, 0, 1)',
                        'rgba(128, 128, 128, 1)',
                        'rgba(211, 211, 211,1)'

                    ],
                    borderColor: [
                        'rgba(248, 134, 34, 1)',
                        'rgba(0, 0, 0, 1)',
                        'rgba(128, 128, 128, 1)',
                        'rgba(211, 211, 211,1)'

                    ],
                    borderWidth: 1
                }]

            },
            options: {
                responsive: true
            }
        });
    });
});