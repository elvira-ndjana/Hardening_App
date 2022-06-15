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



    $(".executer").click(function(){
        execution = true;
        $(".msgProcedure").removeClass("text-orange").addClass("text-warning").show().html('Veuillez patienter...');
        ip = $("#ip").val();
        type = $("#type").val();
        procedure = "";
        for(i in $("#procedure").val())
            procedure += $("#procedure").val()[i] +","
        email = $("#email").val();
        $.get("../executer_verification/",{ip: ip, type: type, procedure: procedure, email: email},
        function(data){
            if(data.status==200){
                $.post("/procedures/correctionNonConformite/",{ip: ip, type: type, procedure: data.conformites,
                email: email,csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
                function(data){});
                $(".msgProcedure").on("click",".conformites", function(){
                    window.location.href = "/procedures/correctionNonConformite/";
                });
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
          $.get("../avancementVerification/",{},function(data){
            $(".progress-bar").css("width",data.pourcentage+"%").text(data.pourcentage.toFixed(2)+"%");
            if( data.pourcentage.toFixed(2) == 100.00){
                message = '<center> Félicitation, votre Opération est terminée.</center>';
                message += 'Total des commandes : '+data.total+' <br/>';
                message += 'Nombre de commande éffectuée : '+data.effectue+' <br/>';
                message += 'Nombre de conformités : '+data.conformite+' <br/>';
                if(data.conformite==0)
                    message += '<button class="btn btn-orange mt-1 terminer-execution"> D\'accord </button>';
                else
                    message += '<button class="btn btn-orange mt-1 conformites">Aller aux non conformité </button>';
                $(".msgProcedure").show().html(message);
            }
            else if( data.pourcentage.toFixed(2) != 0.00){
                message = '<center class="fw-bolder"> Opération en cours de Traitement...</center>';
                message += 'Total des commandes : '+data.total+' <br/>';
                message += 'Nombre de commande éffectuée : '+data.effectue+' <br/>';
                message += 'Nombre de conformités : '+data.conformite+' <br/>';
                $(".msgProcedure").show().html(message);
            }
        });
      }
    },1000);

});