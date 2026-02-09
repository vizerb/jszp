## Egyszerű jszp lekérdező
- Csak a releváns adatokat jeleníti meg
- Visszaszámol 30mp-et a kérések között

### Program használata
Cloneold, vagy töltsd le a repositoryt, majd a gyökérkönyvtárban nyiss egy powershell terminált és futtasd az alábbiakat
- Előkészítés (csak egyszer kell):
  1. Python telepítése:
  ```
  winget install -e --id Python.Python.3.11
  ```
  
  2. Scriptek futtatásához engedély:
  ```
  Get-ChildItem -Path "./" -Recurse | Unblock-File
  ```
  
  3. Függőségeket letöltő setup script:
  ```
  .\setup.ps1
  ```
- Használat:
  ```
  .\run.ps1
  ```
