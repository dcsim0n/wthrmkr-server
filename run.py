#
# WTHR MKR server
# Tim Walter & Dana Simmons 2019
#

from app import app

# SSL = adhoc generates a new ssl cert every time the app runs
# should be replaced with a certificate when deployed
app.run( host="0.0.0.0", port=3000, debug=True, ssl_context="adhoc" )