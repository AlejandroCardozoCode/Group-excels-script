from pathlib import Path
import pandas as pd


def searchFilesInFolder(folderPath, listOfExt):
    # obtener todas las sub carpetas de este directorio
    folderPath = Path(folderPath)
    allDirectories = set(folderPath.rglob("**/"))
    totalFilesNumber = 0
    # lista de listas donde en cada posición están los archivos validos por cada carpeta
    listOfFilesPath = []
    for directory in list(allDirectories):
        # reiniciar listas
        filesInDirectory = set()
        validFiles = set()

        # buscar archivos con extenciones validas
        for ext in listOfExt:
            filesInDirectory.update(directory.glob(ext,))
        
        # continuar con la siguiente iteracion si no hay archivos validos            
        if(len(filesInDirectory)==0):
            continue

        for file in list(filesInDirectory):
            #Agregar la ruta del audio actual a las canciones validas
            if not file.parts[-1].startswith('.'):
                validFiles.add(file.absolute().as_posix())
                totalFilesNumber += 1 

        listOfFilesPath.append(list(validFiles))


    return listOfFilesPath, totalFilesNumber

folderPath = input("ingrese la ruta de la carpeta: ")
extFormat = input("ingrese el formato de la extension: ")
listOfExcelsPath, total = searchFilesInFolder(folderPath=folderPath, listOfExt=[extFormat])
combinedExcel = pd.DataFrame()

if len(listOfExcelsPath) == 0:
    exit()

for index, path in enumerate(listOfExcelsPath):
    print("Procesando excel #", index, " de ", len(listOfExcelsPath))
    df = pd.read_excel(path[0], usecols=lambda x: x != 0)
    # Combinar todos los DataFrames en uno solo
    combinedExcel = pd.concat([combinedExcel, df], ignore_index=True)

exportPath = Path(folderPath) / "Final.xlsx"
combinedExcel.to_excel(exportPath)