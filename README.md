<h1>JourneyScienceApi</hi>

<h2>A microservice written in Flask with Python3.6+</h2>

<h3>To run locally:</h3>
(Assumed to be have python3.6+ and associated pip available in current working path)
<br>
$python3.6 -m venv &lt;directory&gt; will initialize a python3.6 virtual environment in &lt;directory&gt; <br>
and $source &lt;directory&gt;/bin/activate will activate it
<br>
<ol>
    <li>$ ./setup.sh</li>
    <li>Create and adjust env.sh in root directory 
    (/some/path/to/journey_science) 
    Recommend using env.sh.template as a boilerplate
    <li>$ npm install (may need to update node if you get errors)</li>
    <li>$ gulp (the above step should have installed it but if not npm install -g gulp will work, or however else you want to install gulp)</li>
    <li>$ source env.sh </li>
    <li>$ alembic upgrade heads</li>
    <li>(Optional)$ python run_app_tests.py (runs unittest in app context) OR python -m unittest (but that will fail on some app unittests)</li>
    <li>$ python run.py</li>
</ol>


<h4>Note</h4>
<p>in models/calls/upload.py, the __tableargs__ definition is commented out. This is a developmental change, sqlite does not support schemas, so when the ORM adds the schema name in the query, it all goes haywire. If you choose to use a different database, please uncomment it! </p>

<h4>Things left to do</h4>
<ul>
    <li>Some async task runnner like celery, to handle the aggregating</li>
    <li>Refactor/clean up the aggregator class, that thing is... unwieldy</li>
    <li>Better running script so less things to type when running</li>
    <li>Deployment setup, automated, ideally</li>
</ul>
