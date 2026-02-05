## Egyszerű jszp lekérdező
- Csak a releváns adatokat jeleníti meg
- Visszaszámol 30mp-et a kérések között

### Program használata

Cloneold, vagy töltsd le a repositoryt, majd a gyökérkönyvtárban nyiss egy powershell terminált és futtasd az alábbiakat
1. Python telepítése:
```
winget install -e --id Python.Python.3.11
```

2. Scriptek futtatásához engedély:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

3. Futtasd a setup scriptet (egyszer kell csak futtatni):
```
.\setup.ps1
```

4. Futtasd az indító powershell scriptet:
```
.\run.ps1
```
