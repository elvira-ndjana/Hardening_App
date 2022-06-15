$(document).ready(function (){
    var execution = false; // pour modifier le statut de la barre

    $("#type").click(function(){
        $("#type").click(function(){
        $("#procedure").html("")
            $.get("../rechercheProcedure/",{equipement: $("#type").val()},
            function(data){
                donnees = "";
                if(data.procedure.length!=0)
                        donnees += '<option  value="Tout" >Tout</option>';
                for( i in data.procedure){
                    donnees += '<option  value="'+data.procedure[i].id+'" >'+data.procedure[i].nom+'</option>';
                }
                $("#procedure").html(donnees)
            });
        });
        return false;
    });
    $(".executer-conformite").click(function(){
        execution = true;
        $(".msgProcedure").show().html('Veuillez patienter...');
        ip = $("#ip").val();
        type = $("#type").val();
        procedure = $("#procedure").val()
        email = $("#email").val();
        $.get("../executerConformite/",{ip: ip, type: type, procedure: procedure, email: email},
        function(data){
            if(data.status==200){

            }else{
                message = '<center>'+data.message+'</center>'
                console.log(data.message)
                $(".msgProcedure").show().html(message);
            }
        });
        return false;
    });

    $(".executer").click(function(){
        execution = true;
        $(".msgProcedure").removeClass("text-orange").addClass("text-warning").show().html('Veuillez patienter...');
        ip = $("#ip").val();
        type = $("#type").val();
        procedure = "";
        for(i in $("#procedure").val())
            procedure += $("#procedure").val()[i] +","
        email = $("#email").val();
        $.get("../executerProcedure/",{ip: ip, type: type, procedure: procedure, email: email},
        function(data){
            if(data.status==200){

            }else{
                message = '<center>'+data.message+'</center>'
                console.log(data.message)
                $(".msgProcedure").removeClass("text-orange").addClass("text-warning").show().html(message);

            }
        });
        return false;
    });

    $(".effacer").click(function(){
        execution = false;
        $("#ip").val("");
        $("#type").val("");
        $("#procedure").html("")
        $("#procedure").val("")
        $("#email").val("");
        $(".msgProcedure").hide();
        return false;
    });

    $(".progressement").on("click",".terminer-execution",function(){
        execution = false;
        $(".progress-bar").css("width","0%").text("0%");
        $("#ip").val("");
        $("#type").val("");
        $("#procedure").val("")
        $("#procedure").html("")
        $("#email").val("");
        $(".msgProcedure").removeClass("text-warning").addClass("text-orange").html("").hide();
    });

    setInterval(function(){
      if(execution == true){
          $.get("../avancementProcedure/",{},function(data){
            $(".progress-bar").css("width",data.pourcentage+"%").text(data.pourcentage.toFixed(2)+"%");
            if( data.pourcentage.toFixed(2) == 100.00){
                message = '<center> Félicitation, votre Opération est terminée.</center>';
                message += 'Total des commandes : '+data.total+' <br/>';
                message += 'Nombre de commande éffectuée : '+data.effectue+' <br/>';
                message += '<button class="btn btn-orange mt-1 terminer-execution"> D\'accord </button>';
                $(".msgProcedure").show().html(message);
            }
            else if( data.pourcentage.toFixed(2) != 0.00){
                message = '<center class="fw-bolder"> Opération en cours de Traitement...</center>';
                message += 'Total des commandes : '+data.total+' <br/>';
                message += 'Nombre de commande éffectuée : '+data.effectue+' <br/>';
                $(".msgProcedure").show().html(message);
            }
        });
      }
    },1000);

});