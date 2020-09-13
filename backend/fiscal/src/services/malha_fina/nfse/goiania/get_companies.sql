SELECT c.code, c."name", c.cgce, c."dateInicialAsClient", c."dateFinalAsClient" 
  FROM companies_goiania cg 
       INNER JOIN companies c 
            ON    c.code = cg.code 
 WHERE ( c.code LIKE '#' )
   AND ( c."dateInicialAsClient" IS NULL OR c."dateInicialAsClient" <= '#' )
   AND ( c."dateFinalAsClient" IS NULL OR c."dateFinalAsClient" >= '#' )
   AND ( c.cgce LIKE '#' )
ORDER BY c.code