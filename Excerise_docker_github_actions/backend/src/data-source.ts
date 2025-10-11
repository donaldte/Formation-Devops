import { DataSource } from "typeorm";
import { User } from "./entities/User";
import "dotenv/config";

export const dataSource = new DataSource({
  //your app may require a URL. this container setup does not.
  type: "postgres", //type will always be set to postgres
  port: 5432, //default port for postgres is 5432, can also use env variable set in docker-compose
  host: process.env.PG_HOST,
  database: process.env.PG_DATABASE,
  username: process.env.PG_USERNAME,
  password: process.env.PG_HOST,
  logging: true, // can be set to false if logging isn't necessary for your app
  synchronize: true, //creates tables automatically, no need for running a migration
  entities: [User], //add more entities here if needed
});
