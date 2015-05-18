Script iniciado em Seg 18 Mai 2015 18:05:12 BRT
]0;davidcmm@betara: /local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuariosdavidcmm@betara:/local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuarios$ ./executaQScore.sh [1@R[KRscript analisaICPorFoto.R allSolteiroOrdInter. dat allCasadoOrdInter.dat solteiro casado
]0;davidcmm@betara: /local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuariosdavidcmm@betara:/local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuarios$ ls
adulto.dat                            firsJovemOrd.dat                      jovem.dat                       rgbQScoreAgradSolteiro.dat
alta.dat                              firsJovemOrdInter.dat                 [0m[01;32mkendallDistance.R[0m               rgbQScoreSegAdulto.dat
[01;32manalisaCorrelacao.R[0m                   firsLiberdadeOrd.dat                  krippAll.dat                    rgbQScoreSegAllAdulto.dat
[01;32manalisaICPorFoto.R[0m                    firsLiberdadeOrdInter.dat             krippAll.dat~                   rgbQScoreSegAllBaixa.dat
[01;32manalisaICPorFoto.R~[0m                   firsMasculinoOrd.dat                  [01;32mkrippMoran.R[0m                    rgbQScoreSegAllCasado.dat
[01;32manalisaQScorePorBairro.py[0m             firsMasculinoOrdInter.dat             [01;32mkrippMoran.R~[0m                   rgbQScoreSegAllCatole.dat
[01;32manalisaQScore.py[0m                      firsMediaOrd.dat                      liberdade.dat                   rgbQScoreSegAllCentro.dat
[01;32manalisaQScore.py~[0m                     firsMediaOrdInter.dat                 lines.dat                       rgbQScoreSegAllFeminino.dat
[01;32manalisaRegressao.R[0m                    firsNotCatoleOrd.dat                  masculino.dat                   rgbQScoreSegAllJovem.dat
[01;32manalisaTudo.sh[0m                        firsNotCatoleOrdInter.dat             media.dat                       rgbQScoreSegAllMasculino.dat
[01;32manalisaTudo.sh~[0m                       firsNotCentroOrd.dat                  notcatole.dat                   rgbQScoreSegAllMedia.dat
baixa.dat                             firsNotCentroOrdInter.dat             notcentro.dat                   rgbQScoreSegAllNotCatole.dat
[01;32mcalculaTTest.R[0m                        firsNotLiberdadeOrd.dat               notliberdade.dat                rgbQScoreSegAllNotCentro.dat
casado.dat                            firsNotLiberdadeOrdInter.dat          [01;32mopinioesPorFoto.py[0m              rgbQScoreSegAllSolteiro.dat
catole.dat                            firsSolteiroOrd.dat                   [01;32mopinioesPorFoto.py~[0m             rgbQScoreSegBaixa.dat
centro.dat                            firsSolteiroOrdInter.dat              [01;32mpreparaConsenso.py[0m              rgbQScoreSegCasado.dat
[01;32mcombinaRGBQScoreLinhas.py[0m             firstAdulto.dat                       [01;32mpreparaConsenso.py~[0m             rgbQScoreSegCatole.dat
consenseMatrixAgraAdulto.dat          firstBaixa.dat                        [01;32mpreparaHTML.py[0m                  rgbQScoreSegCentro.dat
consenseMatrixAgraCasado.dat          firstCasado.dat                       [01;32mpreparaHTML.py~[0m                 rgbQScoreSegFeminino.dat
consenseMatrixAgraCasadoSolteiro.dat  firstCatole.dat                       [01;32mpreparaSVMInput.py[0m              rgbQScoreSegJovem.dat
consenseMatrixAgraJovemAdulto.dat     firstCentro.dat                       [01;32mprocessInputLatLong.sh[0m          rgbQScoreSegMasculino.dat
consenseMatrixAgraJovem.dat           firstFeminino.dat                     [01;34mrankings[0m                        rgbQScoreSegMedia.dat
consenseMatrixAgraSolteiro.dat        firstJovem.dat                        rgb.dat                         rgbQScoreSegNotCatole.dat
consenseMatrixSegAdulto.dat           firstLiberdade.dat                    rgbQScoreAgradAdulto.dat        rgbQScoreSegNotCentro.dat
consenseMatrixSegCasado.dat           firstMasculino.dat                    rgbQScoreAgradAllAdulto.dat     rgbQScoreSegSolteiro.dat
consenseMatrixSegCasadoSolteiro.dat   firstMedia.dat                        rgbQScoreAgradAllBaixa.dat      runAdulto.csv
consenseMatrixSegJovemAdulto.dat      firstNotCatole.dat                    rgbQScoreAgradAllCasado.dat     runBaixa.csv
consenseMatrixSegJovem.dat            firstNotCentro.dat                    rgbQScoreAgradAllCatole.dat     runCasado.csv
consenseMatrixSegSolteiro.dat         firstNotLiberdade.dat                 rgbQScoreAgradAllCentro.dat     runCatole.csv
[01;34mcorrelacao[0m                            firstSolteiro.dat                     rgbQScoreAgradAllFeminino.dat   runCentro.csv
[01;32mencontraInterseccao.py[0m                [01;34mIC[0m                                    rgbQScoreAgradAllJovem.dat      run.csv
[01;32mexecutaQScore.sh[0m                      [01;34midsGrupos[0m                             rgbQScoreAgradAllMasculino.dat  runFeminino.csv
[01;32mextractLatLongStreet.py[0m               intersectionAllBaixaMedia.dat         rgbQScoreAgradAllMedia.dat      runJovem.csv
feminino.dat                          intersectionAllCatole.dat             rgbQScoreAgradAllNotCatole.dat  runLiberdade.csv
firsAdultoOrd.dat                     intersectionAllCentro.dat             rgbQScoreAgradAllNotCentro.dat  runMasculino.csv
firsAdultoOrdInter.dat                intersectionAllFemininoMasculino.dat  rgbQScoreAgradAllSolteiro.dat   runMedia.csv
firsBaixaOrd.dat                      intersectionAllJovemAdulto.dat        rgbQScoreAgradBaixa.dat         runNotCatole.csv
firsBaixaOrdInter.dat                 intersectionAllLiberdade.dat          rgbQScoreAgradCasado.dat        runNotCentro.csv
firsCasadoOrd.dat                     intersectionAllSolteiroCasado.dat     rgbQScoreAgradCatole.dat        runNotLiberdade.csv
firsCasadoOrdInter.dat                intersectionBaixaMedia.dat            rgbQScoreAgradCentro.dat        runSolteiro.csv
firsCatoleOrd.dat                     intersectionCatole.dat                rgbQScoreAgradFeminino.dat      [01;32mselectRunPerUsers.py[0m
firsCatoleOrdInter.dat                intersectionCentro.dat                rgbQScoreAgradJovem.dat         solteiro.dat
firsCentroOrd.dat                     intersectionFemininoMasculino.dat     rgbQScoreAgradMasculino.dat     testeMasc.dat
firsCentroOrdInter.dat                intersectionJovemAdulto.dat           rgbQScoreAgradMedia.dat         teste.txt
firsFemininoOrd.dat                   intersectionLiberdade.dat             rgbQScoreAgradNotCatole.dat     usersInfo.dat
firsFemininoOrdInter.dat              intersectionSolteiroCasado.dat        rgbQScoreAgradNotCentro.dat
]0;davidcmm@betara: /local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuariosdavidcmm@betara:/local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuarios$ ls IC/
allICAdultoCat.dat     allICCasadoCat.dat       allICJovemCat.dat         allICMediaCat.dat        IC adulto jovem .pdf
allICAdultoCentro.dat  allICCasadoCentro.dat    allICJovemCentro.dat      allICMediaCentro.dat     IC baixa media .pdf
allICAdulto.dat        allICCasado.dat          allICJovem.dat            allICMedia.dat           IC feminino masculino .pdf
allICAdultoLib.dat     allICCasadoLib.dat       allICJovemLib.dat         allICMediaLib.dat        IC solteiro casado .pdf
allICBaixaCat.dat      allICFemininoCat.dat     allICMasculinoCat.dat     allICSolteiroCat.dat
allICBaixaCentro.dat   allICFemininoCentro.dat  allICMasculinoCentro.dat  allICSolteiroCentro.dat
allICBaixa.dat         allICFeminino.dat        allICMasculino.dat        allICSolteiro.dat
allICBaixaLib.dat      allICFemininoLib.dat     allICMasculinoLib.dat     allICSolteiroLib.dat
]0;davidcmm@betara: /local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuariosdavidcmm@betara:/local/david/pybossa_env/campinaPulse/scripts/analise/dadosMaio15/usuarios$ git add analisaTudo.sh.[K analisaICPorFoto.R preparraC