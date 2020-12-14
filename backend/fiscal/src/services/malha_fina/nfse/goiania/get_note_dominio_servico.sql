SELECT ser.codi_emp, ser.codi_ser, ser.nume_ser, ser.vcon_ser, ser.ddoc_ser, ser.situacao_ser AS situacao,
       ser.codi_acu, ser.codi_cli, cli.nome_cli, cli.cgce_cli
  FROM bethadba.efservicos AS ser
       INNER JOIN bethadba.efclientes AS cli
            ON    cli.codi_emp = ser.codi_emp
              AND cli.codi_cli = ser.codi_cli
 WHERE ser.codi_emp = #
   AND ser.nume_ser = #
   AND cli.cgce_cli = '#'