import requests
import codecs

query1 = """<union>
<query type="way">
  <has-kv k="addr:full"/> 
  <has-kv k="addr:city"/>
  <has-kv k="addr:street"/>
  <bbox-query e="%s" n="%s" s="%s" w="%s"/>
  </query>
<query type="node">
  <has-kv k="addr:full"/> 
  <has-kv k="addr:city"/>
  <has-kv k="addr:street"/>
  <bbox-query e="%s" n="%s" s="%s" w="%s"/>
</query>
</union>

<print/>""" % ((-86.805193, 47.080799, 42.491920, -92.889259) * 2)
r1 = requests.post('http://overpass-api.de/api/interpreter/', data=query1)

f = open("osm_data.xml", "w")
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
r2 = requests.post('http://overpass-api.de/api/interpreter/', data=query2)

f = codecs.open("osm_data_street.xml", "wb", "utf-8")
r2.encoding = 'utf-8'
f.write(r2.text)
