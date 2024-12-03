<h1>1.</h1>
<h2>To Run Flask Server:</h2>
<ul>
<l1>
venv/Scripts/activate </li>
<li>
pip install -r requirements.txt
</li>
<li>python app.py</li>
</ul>

<h1>2.</h1>
<h2>To Run Redis-Server:</h2>
<ul>

<li>
ubuntu 22.04 WSL

</li>
<l1>
source venvu/bin/activate </li>
<li>redis-server</li>
</ul>

<h1>3.</h1>
<h2>Celery Worker:</h2>
<ul>
<l1>
celery -A main:celery_app worker --loglevel INFO
 </li>
</ul>

<h1>4.</h1>
<h2>Celery Beat:</h2>
<ul>
<l1>
celery -A main:celery_app beat --loglevel INFO
 </li>
</ul>

<h1> 5. </h1>
<h2>Mail HOg </h2>
<ul>
<li>
~/go/bin/MailHog
</li>
</ul>
<h1> 6. </h1>
<h2>Run FrontEnd </h2>
<ul>
<li>
cd frontend
</li>
<li>
npm install
npm run dev
</li>
</ul>

