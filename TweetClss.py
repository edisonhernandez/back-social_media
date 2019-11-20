class TweetG:
    def __init__(self,created_at,name,username,text,location,coordinates,place,retweet_count,statuses_count,followers_count,friends_count,url):
        self.created_at = created_at
        self.name = name
        self.username = username
        self.text = text
        self.location = location
        self.coordinates = coordinates
        self.place = place
        self.retweet_count = retweet_count
        self.statuses_count = statuses_count
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.url = url
#fecha de creacion del tweet
#NOMBRE REAL
#NOMBRE DE USUARIO
#texto
#localizacion en palabras (Quito - Ecuador)
#Representa la ubicación geográfica de este Tweet
# Cuando está presente, indica que el tweet está asociado (pero no necesariamente desde) un Lugar 
#contador de cuantas veces de retweeteo el texto
#numero de tweets realizados por el usuario
#numero de seguidores
#numero de amigos (siguiendo)
#url del tweet
