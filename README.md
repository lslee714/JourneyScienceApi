<h1>JourneyScienceApi</hi>

<h2>A microservice written in Flask with Python3.6+</h2>

(Assumed to be have python3.6+ and associated pip available in current working path)
<br>
<br>
<a href='https://docs.python.org/3.6/library/venv.html'>Here's how you can create a virtual environment in python</a>
<br>
<br>
<h3>Setting up Application</h3>
<ol>
    <li>$ ./setup.sh</li>
    <li>Create and adjust an environment file (e.g. env.sh) in root directory 
    (/some/path/to/journey_science) 
    Recommend using env.sh.template as a boilerplate
    Example of database uri: "[sql db type]:///path/to/db", e.g. "sqlite:////$(pwd)/test.db"
    <li>$ npm install (may need to update node if you get errors)</li>
    <li>$ gulp (the above step should have installed it but if not npm install -g gulp will work, or however else you want to install gulp)</li>
    <li>$ source env.sh (or file from step #2)</li>
    <li>$ alembic upgrade heads</li>
</ol>

<h3>Running the application</h3>
<ol>
    <li>$ source env.sh (If environment not loaded) 
    <li> <strong>*</strong>  $ python run_app_tests.py 
        (runs unittest in app context) OR $ python -m unittest (but that will fail on some app unittests) 
    </li>
    <li>$ python run.py</li>
</ol>

<h3>Running the celery worker</h3>
<ol>
    <li>TODO - outline here </li>    
</ol>

<strong>*</strong> Optional step

<h4>Note</h4>
<p>In models/calls/upload.py, the __tableargs__ definition is commented out. This is a developmental change, sqlite does not support schemas, so when the ORM adds the schema name in the query, it all goes haywire. If you choose to use a different database, please uncomment it! </p>

<h4>Things left to do</h4>
<ul>
    <li>Deployment setup, automated, ideally</li>
</ul>
