SELECT ent.codi_emp, ent.codi_ent, ent.nume_ent, ent.vcon_ent, ent.ddoc_ent, ent.situacao_ent AS situacao,
       ent.codi_acu, ent.codi_for, forn.nome_for, forn.cgce_for
  FROM bethadba.efentradas AS ent
       INNER JOIN bethadba.effornece AS forn
            ON    forn.codi_emp = ent.codi_emp
              AND forn.codi_for = ent.codi_for
 WHERE ent.codi_emp = #
   AND ent.nume_ent = #
   AND forn.cgce_for LIKE '%' + SUBSTR('#', 1, len(forn.cgce_for)) + '%'