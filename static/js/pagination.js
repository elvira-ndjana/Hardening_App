function pagination() {
                            const argent = new Intl.NumberFormat('fr-FR', {
                                minimumFractionDigits: 0
                            });
                            var table = $("#tableau");
                            var maxligne = 9;
                            var totalligne = $("#contenu-table tr").length - 1;
                            $(".totals").text(totalligne);
                            if ($(".table-vente tr:visible").length != "undefined") {
                                somme = 0;
                                for (var i = 0; i < $(".table-vente tr").length - 1; i++) {
                                    var tab = $("#contenu-table tr:eq(" + i + ") td:eq(4)").html();
                                    var prixx = tab.split(" ");
                                    somme = somme + parseInt(prixx[0]);
                                }
                                $(".totalven").text(argent.format(somme))
                            }

                            function visiblepage(page) {
                                var id = 0;
                                $("#contenu-table tr").each(function() {
                                    id++;
                                    if (id > (maxligne * page) || id < (maxligne * (page - 1)) + 1)
                                        $(this).hide();
                                    else {
                                        $(this).show();
                                    }
                                });
                                $("#contenu-table tr:last").show()
                            }
                            for (var i = 0; i < $("#contenu-table tr:visible").length; i++) {
                                $("#contenu-table tr:eq(" + i + ") td a").removeAttr("pos").attr("pos", i);
                            }
                            /* les pages  */
                            if ($(".table-stock tr").length != 0)
                                var affhtml = '<li class="page-item old"><a class="page-link" href="#"><</a></li>';
                            else
                                var affhtml = '<li class="page-item old"><a class="page-link" href="#">Précédent</a></li>';
                            var nbrepage = Math.ceil(totalligne / (maxligne));
                            console.log("nbre ligne " + nbrepage);
                            for (var i = 1; i <= nbrepage; i++) {
                                affhtml = affhtml + '<li class="page-item" data-page="' + i +
                                    '" ><a class="page-link" href="#">' + i + '</a></li>';
                            }
                            if ($(".table-stock tr").length != 0)
                                affhtml = affhtml + '<li class="page-item next"><a class="page-link next" href="#">></a></li>';
                            else
                                affhtml = affhtml + '<li class="page-item next"><a class="page-link next" href="#">Suivant</a></li>';
                            if (nbrepage != 1)
                                $(".pagination").html(affhtml);

                            //--------------------------------------
                            function affichepagi(page) {
                                $("li[data-page]").removeClass("active");
                                $("li[data-page]").hide();
                                var max = 0;
                                var pag = page - 2;
                                if (page == 1) pag = page;
                                if (page == 2) pag = page - 1;
                                if (page > 4 && page == nbrepage) pag = page - 4;
                                if (page > 3 && page == nbrepage - 1) pag = page - 3;
                                var i = 0;
                                $(".pagination li[data-page]").each(function() {
                                    i++;
                                    if (max < 5) {
                                        if (pag == i) {
                                            $(this).show();
                                            max++;
                                            pag++;
                                        }
                                    }
                                });
                                visiblepage(page);
                                if (page == 1)
                                    $("li.old").addClass("disabled");
                                else
                                    $("li.old").removeClass("disabled");
                                if (page == nbrepage)
                                    $("li.next").addClass("disabled");
                                else
                                    $("li.next").removeClass("disabled");

                                $("li[data-page='" + page + "']").addClass("active");
                            }
                            affichepagi(1);
                            $("li[data-page]").click(function() {
                                affichepagi($(this).attr('data-page'));
                            });
                            $("li.next").click(function() {
                                var x = parseInt($(".pagination li.active").attr('data-page')) + 1;
                                if (x - 1 < nbrepage)
                                    affichepagi(x);
                            });
                            $("li.old").click(function() {
                                var x = parseInt($(".pagination li.active").attr('data-page')) - 1;
                                if (x > 0)
                                    affichepagi(x);
                            });
                            // pour permettre au dom de leur detecter les nouveau tr pour la page reglage

                        }