# contract type, ticker symbol, open date, close date
# C	XYZ	2022-03-01	2022-03-27

import fileinput
import random
from hashlib import md5
from mykey import mykey
from datetime import date, timedelta


# obscure symbols
uniq_symbols = set()
fh = open('symbol_lookup', 'w')
def obhash(symbol):
  s = symbol + mykey
  obsymbol = md5(s.encode('utf-8')).hexdigest()
  if symbol not in uniq_symbols:
    fh.write("{}\t{}\n".format(symbol, obsymbol))
    uniq_symbols.add(symbol)
  return obsymbol


# jitter dates
def jitter(od, cd):
  jit = random.randrange(7)
  if random.choice([0,1]) > 0:
    od += timedelta(days=jit)
    cd += timedelta(days=jit)
  else:
    od -= timedelta(days=jit)
    cd -= timedelta(days=jit)
  return od, cd


# print template of html file
print("<html>")
print("  <head>")
print("    <script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>")
print("    <script type=\"text/javascript\">")
print("      google.charts.load('current', {'packages':['timeline']});")
print("      google.charts.setOnLoadCallback(drawChart);")
print("      function drawChart() {")
print("        var container = document.getElementById('timeline');")
print("        var chart = new google.visualization.Timeline(container);")
print("        var dataTable = new google.visualization.DataTable();")
print("")
print("        dataTable.addColumn({ type: 'string', id: 'Ticker' });")
print("        dataTable.addColumn({ type: 'string', id: 'Type' });")
print("        dataTable.addColumn({ type: 'date', id: 'Open Date' });")
print("        dataTable.addColumn({ type: 'date', id: 'Close Date' });")
print("        dataTable.addRows([")


# print timeline table entries based on input
for line in fileinput.input():
  line = line.strip()
  ctype, symbol, open_date, close_date = line.split()
  open_date = date.fromisoformat(open_date)
  close_date = date.fromisoformat(close_date)
  open_date, close_date = jitter(open_date, close_date)
  oy, om, od = str(open_date).split("-")
  cy, cm, cd = str(close_date).split("-")
  print("          [ '{}', '{}', new Date({}, {}, {}), new Date({}, {}, {}) ],".format(obhash(symbol), ctype, oy, om, od, cy, cm, cd))


# print template of html file
print("        ]);")
print("")
print("        chart.draw(dataTable);")
print("      }")
print("    </script>")
print("  </head>")
print("  <body>")
print("   <div id=\"timeline\" style=\"height: 560px;\"></div>")
print("  </body>")
print("</html>")
