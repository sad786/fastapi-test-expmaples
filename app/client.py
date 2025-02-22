import requests as req

res = req.get('http://localhost:8000/users/me/items', headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYXAiLCJleHAiOjE3Mzk1OTAwMjd9.km9pRM6Np4C3jQ7cWNNHsmldbPoR3uKkG14R8yHM07s"})
#res = req.get('http://localhost:8000/users/me/items',headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJhbmdlIiwiZXhwIjoxNzM5NTkwNzA4fQ.65OTz9IRFCb3zrsyP3DahvbQNviNTPtIE8ASzlH5r-k"})
#res = req.post('http://localhost:8000/token/', data={"username":"strange","password":"str123"})

#res = req.get('http://localhost:8000/users/me/items', headers={"Authorization":""})

print(res.status_code, res.content)