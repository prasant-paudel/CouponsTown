var req = new XMLHttpRequest()
req.open('GET', '/api/?command=validate')
req.send()

req.open('GET', '/api/?command=update_ratings')
req.send()