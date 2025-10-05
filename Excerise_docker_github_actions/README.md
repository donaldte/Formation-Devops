# Docker example

## This is an example template for how to dockerize your multi-container, full-stack Node.js application. 

This example inclues Postgres, Redis, pgAdmin4, and a separate frontend and backend on different ports. The application itself doesn't do much, but it will connect to a postgres database via typeorm as well as a redis database. To run this application, please make sure you have docker installed on your machine. CD into the root directory of the project and type 

> docker-compose up --build

This will build all the images and then compose the multi-container app. 

You can then access the frontend at 

> http://localhost:3000 

and the backend at 

> http://localhost:4000

This is a barebones example designed to help you get your app up and running. While the docker-compose.yml lacks some options that may be required for more complex needs, it will be sufficient for connecting to a postgres database, using cookie-based authentication via redis, and addressing any cors issues which may arise from having a backend and frontend on different ports.

Please let me know if you have any questions or if I can help you!
