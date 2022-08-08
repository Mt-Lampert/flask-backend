# Journal für den Flask REST API Kurs

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
