#! /bin/sh
  #	
  #	Autor: Queiroz
  #	Data : 11/08/94
  #
  #	Este shell script remove a acentuação de um arquivo 
  #	
  
  # A seguir, a localização do arquivo onde se encontram as diretivas
  # para o comando sed
  
  
  # testa se foram fornecidos os arquivos de entrada e saida para
  # o comando. Caso haja erro neste passo emitir a mensagem e encerrar
  # o processamento
  
  if [ $# -lt 2 ]; then
          echo 1>&2 Sintaxe: $0 arquivo_entrada arquivo_saida
          exit 1
  fi
  
  # Atribui à variável infile o primeiro argumento e à variável outfile
  # o segundo argumento
  
  infile=$1
  outfile=$2
  
  # Executa o comando sed para efetuar as substituições
  
  sed -f ./tiraacento.sed $infile > $outfile
