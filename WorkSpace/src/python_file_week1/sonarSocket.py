import socket
from time import sleep

hote='0.0.0.0'
port=1001
connexion_principale=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connexion_principale.bind((hote, port))

fichier=open("data_sonar.txt", "wb")
try:

    while True:
        msg, adress=connexion_principale.recvfrom(65515)
        fichier.write(msg)
        #print(adress, ":",str(msg.decode()))
        #print("--------------------------------------")
        #sleep(3)

except KeyboardInterrupt:
    fichier.close()
    print("Fermeture du fichier !")

except Exception:
    fichier.close()
