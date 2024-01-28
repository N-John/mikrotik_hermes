# mikrotik_hermes
An automated service which is used to manage users connections to mikrotik's hotsport or pppoe service.<br>
<h3>IT SHOULD BE NOTED THAT THIS IS STILL IN CREATION</h3>
<section>
Mikrotik hermes is a python script that works on any mkrotik endpoint which can run python. This service is created for person[s] / businesses using mikrotik hotspot and mikrotik pppoe service as an ISP. It is able to manage a wide number of users matching them to their respective packages and automaticaly manage their subscription periode. It provides a wide variety of tools to interact with the system, the sql and even ssh to the mikrotik from the service itself.<br>
It's simplistic design enables a person with little to no mikroik skills to also operate it and explore the world of mikrotik. It facilitates:<br>
<div>*Mikrotik billing<div>
<div>*Mikrotik automation<div>
<div>*Mikrotik cli<div>
<div>*Mikrotik PPPoE<div>
<div>*Mikrotik Hotspot<div>
<div>*Python scripting<div>
<div>*System administration<div>

</section>
<section>
<h2>REQUIREMENTS & DEPENDANCIES</h2>
<list><div></div>
    <div>*RouterOs with ssh enabled</div>
    <div>*Python</div>
    <div>*Pramiko - This is important as the main service connects to the mikrotik via ssh and stdio</div>
    <div>*Sqlite3 - Used for data storage</div>
    <div>*Terminal - User interuction with service is via cli</div>
</list>
</section>
<br>
<pre>
     +--------------------------------+
     | (1) ADD USER                   |
     | (2) USER COMPENSATION          |
     | (3) USER PAYMENT MANAGEMENT    |
     | (4) SESSION EDIT               |
     | (5) SWITCH TO AUTO_MONITOR     |
     | (6) STATUS                     |
     | (7) MANUAL CLI                 |
     | (8) EXIT                       |
     +--------------------------------+
</pre>
<p>Before use, make sure you edit data on tile named "variables.txt"</p>
<pre>
>>>>FILL IN THE FILLOWING DATA<<<<
+------------------------------------------------+
| DATABASE NAME         |     DATABASE.db        |
+------------------------------------------------+
| LOG FILE NAME         |    log_test.txt        |
+------------------------------------------------+
| MIKROTIK IP           |    192.168.88.1        |
+------------------------------------------------+
| MIKROTIK USERNAME     |    USERNAME            |
+------------------------------------------------+
| MIKROTIK PASSWORD     |    PASSWORD            |
+------------------------------------------------+
</pre>