import requests
import codecs

query1 = """<union>
<query type="way">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:state"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="way">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:city"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="way">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:postcode"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="node">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:state"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="node">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:city"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="node">
    <has-kv k="addr:housenumber"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:type"/>
    <has-kv k="addr:postcode"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
</union>

<print/>""" % ((-70.000000, 50.000000, 25.000000, -125.000000) * 6)
r1 = requests.post('http://overpass-api.de/api/interpreter/', data=query1)
r1.encoding = 'utf-8'

f = codecs.open('data/osm_data.xml', encoding='utf-8' , mode='w+')
f.write(r1.text)


query2 = """<union>
<query type="way">
    <has-kv k="addr:street"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:prefix"/>
    <has-kv k="addr:street:type"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
<query type="node">
    <has-kv k="addr:street"/>
    <has-kv k="addr:street:name"/>
    <has-kv k="addr:street:prefix"/>
    <has-kv k="addr:street:type"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
</union>

<print/>""" % ((-87.61309146881104, 41.890042371392965, 41.87234107841773, -87.64235973358154) * 2)
#r2 = requests.post('http://overpass-api.de/api/interpreter/', data=query2)

#f = codecs.open("data/osm_data_street.xml", "wb", "utf-8")
#r2.encoding = 'utf-8'
#f.write(r2.text)


query3 = """<union>
<query type="way">
    <has-kv k="addr:full" regv="^[0-9]+.*[a-z]+.*[0-9]{5}.*"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
    </query>
<query type="node">
    <has-kv k="addr:full" regv="^[0-9]+.*[a-z]+.*[0-9]{5}.*"/>
    <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
</union>

<print/>
""" % ((-70.000000, 50.000000, 25.000000, -125.000000) * 2)

if __name__ == '__main__' :
    r3 = requests.post('http://overpass-api.de/api/interpreter/', data=query3)

    f = codecs.open("data/osm_data_full_addr.xml", "wb", "utf-8")
    r3.encoding = 'utf-8'
    f.write(r3.text)
