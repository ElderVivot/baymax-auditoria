import os

def readSql(wayFile: str, nameSql: str, *args) -> str:
    # esta função lê um SQL e retorna como string com os *args aplicados. Pro arg ser aplicado tem que colocar um '#' no lugar, 
    # que ele deve fazer a substituição
    sql = ''
    argSequencial = 0
    try:
        with open(os.path.join(wayFile, nameSql), 'rt') as sqlfile:
            for row in sqlfile:
                positionInicialSearchNewHashtag = 0
                rowWithArguments = ''
                positionFindHashtag = row.find('#')
                rowSplit = row
                if positionFindHashtag >= 0:
                    while True:
                        rowWithArguments += f'{rowSplit[:positionFindHashtag]}{args[argSequencial]}'
                        positionInicialSearchNewHashtag = positionFindHashtag+1
                        rowSplit = rowSplit[positionInicialSearchNewHashtag:]
                        positionFindHashtag = rowSplit.find('#')
                        if positionFindHashtag < 0:
                            rowWithArguments += rowSplit                            
                            argSequencial += 1
                            break
                        else:
                            argSequencial += 1
                
                row = rowWithArguments if rowWithArguments != "" else row
                sql += row
    except Exception:
        sql = ''
    
    return sql