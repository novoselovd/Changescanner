import requests
from lxml import etree
from app import db
import models


def run():
    exchangers = models.Exchangers.query.all()
    num_rows_deleted = db.session.query(models.Rates).delete()

    for exch in exchangers:
        try:
            req = requests.get(exch.XMLlink, stream=True)
            req.raw.decode_content = True  # ensure transfer encoding is honoured
            b = etree.parse(req.raw)

            root = b.getroot()

            for i in root.getchildren():
                give = 0.0
                get = 0.0
                if i[0].text == 'QWRUB' and i[1].text == 'SBERRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='QWRUBSBERRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'QWRUB' and i[1].text == 'YAMRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='QWRUBYAMRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'QWRUB' and i[1].text == 'BTC':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='QWRUBBTC', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'QWRUB' and i[1].text == 'WMR':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='QWRUBWMR', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)

                if i[0].text == 'YAMRUB' and i[1].text == 'SBERRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='YAMRUBSBERRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'YAMRUB' and i[1].text == 'QWRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='YAMRUBQWRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'YAMRUB' and i[1].text == 'BTC':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='YAMRUBBTC', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'YAMRUB' and i[1].text == 'WMR':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='YAMRUBWMR', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)

                if i[0].text == 'BTC' and i[1].text == 'SBERRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='BTCSBERRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'BTC' and i[1].text == 'QWRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='BTCQWRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'BTC' and i[1].text == 'YAMRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='BTCYAMRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'BTC' and i[1].text == 'WMR':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='BTCWMR', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)

                if i[0].text == 'SBERRUB' and i[1].text == 'BTC':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='SBERRUBBTC', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'SBERRUB' and i[1].text == 'QWRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='SBERRUBQWRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'SBERRUB' and i[1].text == 'YAMRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='SBERRUBYAMRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'SBERRUB' and i[1].text == 'WMR':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='SBERRUBWMR', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)

                if i[0].text == 'WMR' and i[1].text == 'BTC':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='WMRBTC', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'WMR' and i[1].text == 'QWRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='WMRQWRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'WMR' and i[1].text == 'YAMRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='WMRYAMRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
                if i[0].text == 'WMR' and i[1].text == 'SBERRUB':
                    give = i[2].text
                    get = i[3].text
                    coef = float(float(give)/float(get))
                    new_rate = models.Rates(type='WMRSBERRUB', give=give, get=get, coef=coef, exchangerId=exch.id)
                    db.session.add(new_rate)
        except Exception as e:
            print(exch.name + ' => ' + str(e))

    db.session.commit()
    print('Updated the rates!')