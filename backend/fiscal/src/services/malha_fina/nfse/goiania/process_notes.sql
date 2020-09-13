SELECT *
  FROM notes_nfse nn
 WHERE ( nn."codeCompanie" LIKE '#' )
   AND ( nn."dateNote" BETWEEN '#' AND '#' )
ORDER BY nn."dateNote", nn."numberNote"