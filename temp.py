import models
from app import db

new_exchanger = models.Exchangers(link='https://paymarket.cc', name='Paymarket', description='Test', country='Russia', ownerId=1, XMLlink='https://paymarket.cc/valuta.xml')
new_exchanger1 = models.Exchangers(link='https://obmenmonet.com', name='ObmenMonet', description='Единый обмен валюты', country='Russia', XMLlink='https://obmenmonet.com/exportxml.xml')
#   https://100monet.pro/bestchange.xml
new_exchanger2 = models.Exchangers(link='https://100monet.pro', name='100Monet', description='Самый крутой обменник', country='Russia', XMLlink='https://100monet.pro/bestchange.xml')
#   https://kassa.cc/valuta.xml
new_exchanger3 = models.Exchangers(link='https://kassa.cc', name='Kassa', description='Самый лучший обменник', country='Russia', XMLlink='https://kassa.cc/valuta.xml')
#   https://e-dengi.org/_export/exchange_xml/
new_exchanger4 = models.Exchangers(link='https://e-dengi.org/ru/', name='E-dengi', description='Самый лучший обменник', country='Russia', XMLlink='https://e-dengi.org/_export/exchange_xml/')
#   https://superobmenka.com/ru/export/xml - мало направлений
new_exchanger5 = models.Exchangers(link='https://superobmenka.com/ru/', name='Superobmenka', description='Самый лучший обменник', country='Russia', XMLlink='https://superobmenka.com/ru/export/xml')


db.session.add(new_exchanger)
db.session.add(new_exchanger1)
db.session.add(new_exchanger2)
db.session.add(new_exchanger3)
db.session.add(new_exchanger4)
db.session.add(new_exchanger5)
db.session.commit()
