## Egyszerű jszp lekérdező

- Csak a releváns adatokat jeleníti meg
- Visszaszámol 30mp-et a kérések között

### Program használata

**Használat előtt legalább egyszer be kell lépni a rendes jszp felületbe és el kell fogadni a felhasználói feltételeket.**

Nyiss egy powershell terminált és futtasd az alábbiakat

- Előkészítés (csak egyszer kell):
  1. Python és Git telepítése:

  ```
  winget install -e --id Git.Git Python.Python.3.11
  ```

  2. Forrás letöltése:

  ```
  git clone https://github.com/vizerb/jszp.git
  ```

  3. Gyökérkönyvtárba navigálás:

  ```
  cd jszp
  ```

  4. Függőségeket letöltő setup script futtatása:

  ```
  .\setup.bat
  ```

- Használat:
  ```
  .\run.bat
  ```
