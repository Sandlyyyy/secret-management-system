FROM nginx:alpine

# Копируем фронтенд в контейнер
COPY ../frontend /usr/share/nginx/html

# Копируем конфиг Nginx
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
