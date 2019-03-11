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
    <li>$ source env.sh </li>
    <li>$ alembic upgrade heads</li>
    <li>(Optional)$ python run_app_tests.py (runs unittest in app context) OR python -m unittest (but that will fail on some app unittests)</li>
    <li>$ python run.py</li>
</ol>
