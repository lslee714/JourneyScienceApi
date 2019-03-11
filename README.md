<h1>JourneyScienceApi</hi>

<h2>A microservice written in Flask with Python3.6+</h2>

<h3>To run locally:</h3>
(Assumed to be have python3.6+ and associated pip available in current working path)
<br>
<br>
<ol>
    <li>$ ./setup.sh</li>
    <li>Create and adjust env.sh in root directory 
    (/some/path/to/journey_science) 
    Recommend using env.sh.template as a boilerplate
    <li>$ npm install (may need to update node if you get errors)<li>
    <li>$ gulp (the above step should have installed it but if not npm install -g gulp will work, or however else you want to install gulp)</li>
    <li>$ source env.sh </li>
    <li>$ alembic upgrade heads</li>
    <li>(Optional)$ python run_app_tests.py (runs unittest in app context)</li>
    <li>$ python run.py</li>
</ol>
