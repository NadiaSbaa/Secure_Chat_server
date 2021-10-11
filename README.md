<h1> Secure Chat Server</h1>

<h2>Mission: </h2>
Implementation of a hierarchy of virtual certification entities x509 in openssl in relying on LDAP, in order to create an instant messaging application between clients in the presence of a trusted authority S.

<h2>Technology: </h2>
Python, Crypto, hashlib, tkinter.

<h2>Requirements installation: </h2>
To execute the project you need to install the requirements:
pip install -r requirements.txt


<h2>Execution: </h2>
<h4> 1/ Run the serveur: </h4>  
cd INSAT_PKI <br>
python server_accept_connection_inscription.py

<h4> 2/ Inscription client: </h4>
cd Client <br>
python client_inscription.py

<h4> 3/ Connexion client: </h4>
cd Client <br>
python welcomeClientConnexion.py

<h2>Interface: </h2>
<img src="images/insat2.png" width="700" alt="demo_4">
