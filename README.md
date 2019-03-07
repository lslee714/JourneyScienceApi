<h1>JourneyScienceApi</hi>

<h2>A microservice written in Flask with Python3.6+</h2>

<h3>To run locally:</h3>
(Assumed to be have python3.6+ and pip available in path or in virtual environment )
<br>
<br>
<ol>
    <li>$./setup.sh</li>
    <li>Create and adjust env.sh in root directory 
    (/some/path/to/journey_science) 
    Recommend using env.sh.template as a boilerplate
    <li>$source env.sh
    <li>(Optional)$python -m unittest</li>
    <li>$alembic upgrade heads</li>
    <li>$python run.py or
    if you have a env.sh setup,
    $source env.sh; flask run</li>
</ol>
