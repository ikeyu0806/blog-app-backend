```
docker build -t blog-app-backend .
docker run -d --name blog-app-backend -p 6000:80 blog-app-backend
curl http://127.0.0.1:6000/
curl http://127.0.0.1:6000/items/5?q=somequery
```
