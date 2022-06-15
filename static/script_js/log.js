$(document).ready(function (){

    $(".rechercherlogs").click(function(){
        nettoyer()
        $.get("../recherche_logs/",{date: $("#dateR").val(), user: $("#userR").val(),
        procedure: $("#procedureR").val(), ip: $("#ipR").val()},
        function(data){
            donnees = "";
            for( i in data.logs){
                donnees += '<tr height="40px">';
                donnees += '<th scope="row">'+data.logs[i].id+'</th>';
                donnees += '<td>'+data.logs[i].routine+'</td>';
                donnees += '<td>'+data.logs[i].date+'</td>';
                donnees += '<td>'+data.logs[i].type+'</td>';
                donnees += '<td>'+data.logs[i].ip+'</td>';
                donnees += '<td>'+data.logs[i].user+'</td>';
                donnees += '<td>'+data.logs[i].procedure+'</td>';
                donnees += '<td>';
                donnees += '<span class="flex mt-0">'
                if(data.logs[i].rapport != "")
                    donnees += '<button class="btn-table btn-warning telecharger" width="14px" height="15px" name="'+data.logs[i].rapport+'"> Télécharger </button>'
                donnees += '</span></td></tr>';
            }
            $("#contenu-table").prepend(donnees)
            pagination();
        });
        return false;
    });
    $(".voirListeLogs").click(function(){
        nettoyer()
        $("#dateR").val("")
        $("#userR").val("")
        $("#procedureR").val("")
        $("#ipR").val("")
        $.get("../recherche_logs/",{date: $("#dateR").val(), user: $("#userR").val(),
        procedure: $("#procedureR").val(), ip: $("#ipR").val()},
        function(data){
            donnees = "";
            for( i in data.logs){
                donnees += '<tr height="40px">';
                donnees += '<th scope="row">'+data.logs[i].id+'</th>';
                donnees += '<td>'+data.logs[i].routine+'</td>';
                donnees += '<td>'+data.logs[i].date+'</td>';
                donnees += '<td>'+data.logs[i].type+'</td>';
                donnees += '<td>'+data.logs[i].ip+'</td>';
                donnees += '<td>'+data.logs[i].user+'</td>';
                donnees += '<td>'+data.logs[i].procedure+'</td>';
                donnees += '<td>';
                donnees += '<span class="flex mt-0">'
                if(data.logs[i].rapport != "")
                    donnees += '<button class="btn-table btn-warning telecharger" width="14px" height="15px" name="'+data.logs[i].rapport+'"> Télécharger </button>'
                donnees += '</span></td></tr>';
            }
            $("#contenu-table").prepend(donnees)
            pagination();
        });
        return false;
    });

    $("#contenu-table").on("click",".telecharger", function(){
        console.log("tototo")
        window.location.href = "/static/rapport/"+$(this).attr("name");
        return false;
    });

    function nettoyer(){
        while ($("#contenu-table tr").length>1){
            for(var i=0; i<$("#contenu-table tr").length-1;i++)
                $("#contenu-table tr:eq("+i+")").remove();
        }
    }
});