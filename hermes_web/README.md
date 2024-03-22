# mikrotik_hermes
An automated service which is used to manage users connections to mikrotik's hotsport or pppoe service.<br>
<section>

It's simplistic design enables a person with little to no mikroik skills to also operate it and explore the world of mikrotik. It facilitates:<br>
<div>*Mikrotik billing<div>
<div>*Mikrotik automation<div>
<div>*Mikrotik cli<div>
<div>*Mikrotik PPPoE<div>
<div>*Mikrotik Hotspot<div>
<div>*Python scripting<div>
<div>*System administration<div>
<div>*Payment retriever<div>

</section>
<section>
<p>To use, Run :
<div>Make the set migrations - <code>python manage.py makemigrations</code>
<div>Migrate databases- <code>python manage.py migrate</code></div>
<div>Run server- <code>python manage.py runserver</code></div>
</p>

</section>
<section>
<h2>REQUIREMENTS & DEPENDANCIES</h2>
<list><div></div>
    <div>*RouterOs with ssh enabled</div>
    <div>*Python</div>
    <div>*Django</div>
    <div>*Pramiko - This is important as the main service connects to the mikrotik via ssh and stdio</div>
    <div>*Sqlite3 - Used for data storage</div>
    <div>*Terminal - User interuction with service is via cli</div>
	
</list>
</section>