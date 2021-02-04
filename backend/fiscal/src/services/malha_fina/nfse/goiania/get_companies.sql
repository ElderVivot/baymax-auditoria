SELECT c.code, c."name", c.cgce, COALESCE(c."dateInicialAsClient", DATE('2020-01-01')) AS dateInicialAsClient, COALESCE(DATE(c."dateFinalAsClient") + 1, DATE('2100-01-01')) AS  dateFinalAsClient
  FROM companies_goiania cg 
       INNER JOIN companies c 
            ON    c.code = cg.code 
 WHERE ( c.code LIKE '#' )
   --AND ( c."dateInicialAsClient" IS NULL OR c."dateInicialAsClient" <= '#' )
   --AND ( c."dateFinalAsClient" IS NULL OR c."dateFinalAsClient" >= '#' )
   AND ( c.cgce LIKE '#' )
ORDER BY c.code