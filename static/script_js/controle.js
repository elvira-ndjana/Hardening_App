$(document).ready(function (){
    $(".ajouter-controle").click(function(){
        $("#modaleControle").modal();
        return false;
    });
    $(".annuler-controle").click(function(){
        $("#modaleControle").hide(1000);
        return false;
    });
    $(".enregistrer-controle").click(function(){
        $.get("../recherche_contrôle/",{code: $("#code").val()},function(data){
             if(data.controle.length==0){
                 $.post("../ajouter_contrôle/",{code: $("#code").val(), libelle: $("#libelle").val(), default: $("#default").val(),
                    commande: $("#commande").val(), verification: $("#verification").val(), champVerification: $("#champVerification").val(), procedure: $("#procedure").val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
                    function(data){
                        donnees = "";
                        donnees += '<tr height="40px">';
                        donnees += '<th scope="row">'+data["id"]+'</th>';
                        donnees += '<td>'+data["code"]+'</td>';
                        donnees += '<td>'+data["type"]+'</td>';
                        donnees += '<td>'+data["default"]+'</td>';
                        donnees += '<td>'+data["libelle"]+'</td>';
                        donnees += '<td>'+data["nom"]+'</td>';
                        donnees += '<td>';
                        donnees += '<span class="flex mt-0">'
                        donnees += '<button class="btn-table btn-warning detail" width="14px" height="15px"  identifiant="'+data["id"]+'" name="Détails"> Détail </button>'
                        donnees += '<button class="btn-table btn-warning ms-1 supprimer" width="14px" height="15px"  identifiant="'+data["id"]+'" name="Supprimer"> X </button>'
                        donnees += '</span></td></tr>';

                        $("#contenu-table").prepend(donnees)
                        pagination();
                        $("#code").val("");
                        $("#libelle").val("");
                        $("#default").val("");
                        $("#commande").val("");
                        $("#verification").val("");
                        $("#champVerification").val("");
                        $("#procedure").val("");
                        $(".msgControle").removeClass("text-danger").addClass("text-orange").show().html('<center> le contrôle a bien été enregistré.');
                        setTimeout(function(){
                            $(".msgControle").hide(1000);
                         },2500);
                    });
             }else{
                 $(".msgControle").removeClass("text-orange").addClass("text-danger").show().html('<center> Ce code de contrôle existe déja.');
                setTimeout(function(){
                    $(".msgControle").hide(1000);
                 },2500);
             }
        });
        return false;
    });
    $("#contenu-table").on("click",".detail",function(){ //
        id = parseInt($(this).attr("identifiant"));
        $.get("../recherche_contrôle/",{id: id},function(data){
            $("#codeA").val(data.controle[0].code);
            $("#libelleA").val(data.controle[0].libelle);
            $("#defaultA").val(data.controle[0].default);
            var contenu = ""
            tab = data.controle[0].commande.split(",");
			for(var i=0; i<tab.length;i++){
				contenu += tab[i] + "<br/>";
			}
            $("#commandeA").html(contenu);
            contenu = ""
            tab = data.controle[0].verification.split(",");
			for(var i=0; i<tab.length;i++){
				contenu += tab[i] + "<br/>";
			}
            $("#verificationA").html(contenu);
            contenu = ""
            tab = data.controle[0].champVerification.split(",");
			for(var i=0; i<tab.length;i++){
				contenu += tab[i] + "<br/>";
			}
            $("#champVerificationA").html(contenu);
            $("#procedureA").val(data.controle[0].nom);

        });
        $("#modaleControleAffiche").modal();
        return false;
    });
    $(".annuler-controleA").click(function(){
        $("#modaleControleAffiche").hide(1000);
        return false;
    });
    supprimer = 0 // pas encore possible de le faire
    $("#contenu-table").on("click",".supprimer",function(){
        supprimer = 1;
        $(this).text("Ok");
        boutton = $(this)
        $(this).click(function(){
            if(supprimer==1){
                $.get("../suppression_contrôle/",{id: $(this).attr("identifiant"), },function(data){});
                $(this).parents("tr").remove();
                supprimer = 0
            }
        });
       setTimeout(function(){
            boutton.text("X");
            supprimer = 0
        },5000);
    });

    function nettoyer(){
        while ($("#contenu-table tr").length>1){
            for(var i=0; i<$("#contenu-table tr").length-1;i++)
                $("#contenu-table tr:eq("+i+")").remove();
        }
    }


    $(".rechercherControle").click(function(){
        nettoyer()
        $.get("../recherche_contrôle/",{code: $("#codeR").val(), default: $("#defaultR").val(),
        procedure: $("#procedureR").val(), equipement: $("#equipementR").val()},
        function(data){
            donnees = "";
            for( i in data.controle){
                donnees += '<tr height="40px">';
                donnees += '<th scope="row">'+data.controle[i].id+'</th>';
                donnees += '<td>'+data.controle[i].code+'</td>';
                donnees += '<td>'+data.controle[i].type+'</td>';
                donnees += '<td>'+data.controle[i].default+'</td>';
                donnees += '<td>'+data.controle[i].libelle+'</td>';
                donnees += '<td>'+data.controle[i].nom+'</td>';
                donnees += '<td>';
                donnees += '<span class="flex mt-0">'
                donnees += '<button class="btn-table btn-warning detail" width="14px" height="15px"  identifiant="'+data.controle[i].id+'" name="Détails"> Détail </button>'
                donnees += '<button class="btn-table btn-warning ms-1 supprimer" width="14px" height="15px"  identifiant="'+data.controle[i].id+'" name="Supprimer"> X </button>'
                donnees += '</span></td></tr>';
            }
            $("#contenu-table").prepend(donnees)
            pagination();
        });
        return false;
    });
    $(".voirListeControle").click(function(){
        nettoyer()
        $("#codeR").val("")
        $("#defaultR").val("")
        $("#procedureR").val("")
        $("#defaultR").val("")
        $.get("../recherche_contrôle/",{code: $("#codeR").val(), default: $("#defaultR").val(),
        procedure: $("#procedureR").val(), equipement: $("#equipementR").val()},
        function(data){
            donnees = "";
            for( i in data.controle){
                donnees += '<tr height="40px">';
                donnees += '<th scope="row">'+data.controle[i].id+'</th>';
                donnees += '<td>'+data.controle[i].code+'</td>';
                donnees += '<td>'+data.controle[i].type+'</td>';
                donnees += '<td>'+data.controle[i].default+'</td>';
                donnees += '<td>'+data.controle[i].libelle+'</td>';
                donnees += '<td>'+data.controle[i].nom+'</td>';
                donnees += '<td>';
                donnees += '<span class="flex mt-0">'
                donnees += '<button class="btn-table btn-warning detail" width="14px" height="15px"  identifiant="'+data.controle[i].id+'" name="Détails"> Détail </button>'
                donnees += '<button class="btn-table btn-warning ms-1 supprimer" width="14px" height="15px"  identifiant="'+data.controle[i].id+'" name="Supprimer"> X </button>'
                donnees += '</span></td></tr>';
            }
            $("#contenu-table").prepend(donnees)
            pagination();
        });
        return false;
    });
});