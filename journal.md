# Journal für den Flask REST API Kurs

TODO: 

- [x] einen neuen Git Branch einrichten: _jwt-auth_
- [x] JWT installlieren
- [x] Im `project` package eine Datei `auth.py` einrichten 
- [x] in `auth.py` Users und JWT implementieren
- [x] den JW-Token für User 'Mario' mit `http` ermitteln und in der Datei .env speichern.
- [ ] JWT-Verhalten von `flask-jwt` so weit studieren, dass wir Tests schreiben können.
     - [offizielle Doku](https://pythonhosted.org/Flask-JWT/)
     - [http-jwt-auth](https://github.com/teracyhq/httpie-jwt-auth) als Erweiterung für
       _httpie_ installieren.
     - __Recherche-Ergebnis:__ unautorisierter Zugriff erzeugt einen 401-Error (error: "Authorization required")
- [ ] Tests konzipieren und schreiben
- [ ] in `resources.py` eine neue Ressource `SecretItems` und `SecretItem` implementieren
- [ ] die Route Handler von `SecretItems` und `SecretItem` an JWT binden
- [ ] Die Routen für `SecretItems` bzw `SecretItem`
- [ ] Den _flask\_restful_ branch in _master_ integrieren.


## 2022-08-16

### 16:30

Ich habe mit dem Mocking von `@jwt_required` weitergeforscht. Dabei habe ich folgende 
Entdeckung gemacht:

Im package _flask\_jwt_ findet sich in der Datei `__init.py__` die funktion 
`_jwt_required()`. In der _function description_ steht:

> Does the actual work of verifying the JWT data in the current request. \
> This is done automatically for you by `@jwt_required()` but you could call it manually.\
> Doing so would be useful in the context of optional JWT access in your APIs.

Das heißt nichts anderes als dass das die Funktion ist, die wir mocken müssen.

Das einzige, was sie tut, ist entweder Errors auswerfen oder mit folgender Zeile im 
Request-Kontext einen Wert zuweisen:

```py
from flask import _request_ctx_stack

def _jwt_required(realm):
   # throwing errors
   _request_ctx_stack.top.current_identity = identity = _jwt.identity_callback(payload)
```

Eine Mock-Funktion könnte so aussehen:

```py
from flask import _request_ctx_stack

def _jwt_required_mock(realm):
   # never throwing errors
   _request_ctx_stack.top.current_identity = identity = User(1, "Mario", "s3cr3t")
```


Im Test können wir sie dann wie folgt patchen:

```py
test__mock_jwt_required(mocker):
      mocker.patch(_jwt_required, side_effect=_jwt_required_mock)
```

Das ganze "Verdrahten" muss natürlich auch noch stimmen, aber so könnte es tatsächlich gehen.

Aber vielleicht ist das mit dem _side\_effect_ auch gar nicht nötig. Wenn gesicherte Routen
automatisch freigeschaltet sind in dem Moment, wo keine Errors ausgeworfen werden, genügt auch
dieses Mocking

```py
test__mock_jwt_required(mocker):
      mocker.patch(_jwt_required)
```

### 10:50

Hab JWT in das Projekt integriert bekommen. Hurra!  Allerdings gab es besondere Vorkommnisse:

1. ich musste im Quellcode von `flask_jwt` an zwei Stellen eine kleine Klarstellung 
   vornehmen, und zwar im Verzeichnis `.venv/lib/python3.10/site_packages/jwt/`, dort
   in den Dateien `api_jwt.py` und `api_jws.py`

   ```py
   # vor der Änderung
   from collections import Mapping
   # nach der Änderung
   from collections.abc import Mapping
   ```
   
   Das ist nötig geworden, weil es in Python 3.10 nicht mehr genügt, etwas
   aus dem eigenen _package_ zu importieren -- es muss auch das Modul mit
   dabei stehen.

0. JWT und Authentifizierung brauchen wir nicht testen. Das ist Sache der
   Paket-Entwickler.

0. Problem: Test von Route-Handlern, die mit `@jwt_required` geschützt sind.
   Hier soll Mocking helfen. Die Kundigen bei _stackoverflow_ empfehlen, die
   Funktion zu mocken, die für die Überprüfung des Tokens zuständig ist. 
   Im Falle von `flask_jwt_extended` würde das so aussehen:

   ```py
   mocker.patch(flask_jwt_extended.view_decorators.verify_jwt_in_request)
   ```

## 2022-08-14

### 08:03

Die Idee von vorhin ist voll aufgegangen! Hab sie umgesetzt, und alle Tests 
funktionieren wieder störungsfrei!


### 07:40

Habe DELETE zur den _items_-Routen hinzugefügt. Jetzt hab ich aber ein Problem: 
_Heisenbugs,_, d.h. durch den Umstand, dass ich teste, verändere ich die 
Testumgebung so, dass neue Tests fehlerhafte Ergebnisse liefern.

Grund ist der Umstand, dass ich nicht bei jedem Test mit einem "frischen" 
_item-_set beginne, sondern mit einem Set, dass durch vorangegangene Tests
schon erweitert/geändert -- auf jeden Fall anders ist.  Da muss ich mir was 
einfallen lassen.

Idee: Eine `reset_items()`-Funktion schreiben und sie nach dem `yield` als
cleanup aufrufen.

## 2022-08-13

### 08:15

Hab das Projekt erfolgreich von 'stores' auf 'items' und von _default\_app_ auf 
_restful\_app_ umgestellt. Tests musste ich auch umstellen, aber am Ende ging 
alles glatt.


## 2022-08-12

###  08:55
Der Plan von gestern ist voll aufgegangen! Ich habe gerade eben die Umstellug
eingeleitet und den ersten Test auf _restful\_client_ umgestellt. Der Test
war positiv. Es ist der gleiche Test wie vorher, nur der Weg zur Response war
ein anderer.

Wie Nero Wolfe sagen würde: "Höchst zufriedenstellend!"


## 2022-08-11

Nach Durchsicht von Kapitel 3 und 4 musste ich mir überlegen, wie es mit diesem
Projekt weitergehen soll

Im Kurs wird das Projekt umgestellt auf `flask_restful`. Die Routen und die ganze
Architektur ändert sich damit. Ich habe mich deshalb geweigert, weiter zu arbeiten,
weil ich kein gutes Gefühl bei der Arbeit hatte.

Jetzt habe ich wieder ein gutes Gefühl, weil ich nachgedacht habe und zu einer 
Entscheidung gekommen bin.

> Ich werde in Git einen neuen Branch eröffnen, die bestehenden Tests beibehalten
> und die Migration nach `flask_restful` als riesengroßes Refactoring betrachten.

Die Tests müssen genau so funktionieren wie sie vorher schon funktionieren. Dann
ist die Migration erfolgreich.


## 2022-08-09

### 22:55

Hab jetzt auch die GET-Routen für die Stores fertig. Ich musste mich in einigen
Dingen immer noch orientieren, muss mitdenken, nach-denken, immer neu durchleben,
aber es lohnt sich. Flask war schon immer genau das, was ich als Backend für meine
Frontend-Pläne brauchte, und mit TDD kann ich mich auch noch bei jedem Schritt,
den ich mache, sicher fühlen.


### 18:55

Hab die erste POST-Route fertig. TDD macht Spaß und vertieft das Gelernte sehr,
auch wenn der Weg zum Ergebnis anspruchsvoller ist.

Ein Problem gibt es aber: Durch das Hinzufügen neuer _stores_ zur store-Liste
verändert sich die store-Liste auch im laufenden Testbetrieb. Das hat im
Moment noch keine negativen Auswirkungen, weil ich meine Tests so schreibe, 
dass sie immer funktionieren. Ich weiß aber nicht, wie lange ich das noch 
durchhalten kann.




## 2022-08-08 

### 19:20

Weil wir es noch ein paar Mal öfter brauchen werden, kommt hier eine ausführliche
Dokumentation über das Testen von Flask-Projekten und was es dabei zu beachten
gibt.

Für RESTful APIs ist es als allererstes wichtig, sich über ein paar Punkte klar zu sein:

1. Was wir testen wollen, sind die _responses_ unserer Flask App, und die
   holen wir uns mit Hilfe von _requests._  Dafür brauchen wir eine Flask-Instanz,
   an die wir eine _request_ schicken.  Im vorliegenden Projekt haben wir dafür 
   eine _factory function_ geschrieben 

   ```py
   # file: projects/apps.py
   from flask import Flask, jsonify


    def default_app():
        myApp = Flask(__name__)

        @myApp.route('/')
        def home():
            return jsonify({"message": "Hello, flaskers"})

        return myApp
   ```

2. Tests stehen in einem eigenen Verzeichnis, und es ist wichtig, dass dieses
   Verzeichnis eine eigene `__init__.py`-Datei hat, d.h. dass die Tests als
   eigenes _package_ ausgewiesen werden. Nur so lassen sich Module aus anderen
   _sub-packages_ importieren.

3. Im Testverzeichnis gibt es eine Datei `conftest.py`, in der sog. _fixtures_
   definiert sind. Fixtures sind Funktionen, die bei einem Test als Argumente
   an die Test-Funktion übergeben werden können.  Ihr Rückgabewert kann wie in
   unserem Beispiel direkt im Test Verwendung finden:

   ```py
   # file: tests/conftest.py
   import pytest
   from project import default_app


   @pytest.fixture(scope='module')
   def test_client():
      flask_app = default_app()
      with flask_app.test_client() as test_client:
          # yield, not return!
          yield test_client
    

   # file: tests/test_routes.py
   def test_rootendpoint(test_client):
       """
       GIVEN a default app has been provided
       WHEN we GET the '/' endpoint
       THEN the response status is OK
       AND we find 'flaskers' in the response
       AND we won't find 'Hallo' in the response
       """
       response = test_client.get('/')
       assert response.status_code == 200
       assert 'flaskers' in response.json['message']
       assert 'Hallo' not in response.json['message']
   ```

4. Im Test gibt uns der _test\_client_ die _response_ direkt als Rückgabewert 
   zurück, ohne sie über das Netzwerk zu schicken. Damit können wir sie direkt 
   in unseren Tests verwenden; das _data_-Objekt kann direkt mit Hilfe von 
   `response.json` abgefragt werden.

5. Anders als bei Jest bzw. der testing-library gibt es in _Pytest_ keine
   description, mit der man eine Spec zusammenbauen kann. Wir müssen uns
   zu diesem Zweck mit der _func description_ zufriedengeben und sie wie
   in diesem Fall, im _Gherkin_-Stil formulieren.

### See also

- [Testing Flask Applications](https://flask.palletsprojects.com/en/2.2.x/testing/) 
  aus der offiziellen Flask-Dokumentation.
- Das "Fixtures" Kapitel im PyTest-Buch von Brian Okken.
