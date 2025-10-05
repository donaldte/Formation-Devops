import express from "express";
import "dotenv/config";
import { dataSource } from "./data-source";
import cors from "cors";
import session from "express-session";
import Redis from "ioredis";
import connectRedis from "connect-redis";
import { COOKIE_NAME } from "./constants";

const main = async () => {
  //Initializes the typeorm dataSource asychronously
  dataSource
    .initialize()
    .then(() => {
      console.log("initialized successfully");
    })
    .catch((err) => {
      console.log("data source initialization error occurred: ", err);
    });

  //Creates the express application
  const app = express();

  //basic get request
  app.get("/", (_, res) => {
    res.send("This is a test!");
  });

  //app wil lbe using cors.
  app.use(
    cors({
      origin: process.env.CORS_ORIGIN, //origin can be set to your app specifications.
      credentials: true,
    })
  );

  /**********redis middleware starts here. if adding apollo middleware, this must precede that middleware**/

  // redis@v4, using connectRedis to connect to the session
  const RedisStore = connectRedis(session);

  //any type used as connect-redis types were not up to date for current version
  const redis: any = new Redis(process.env.REDIS_URL as string);

  app.use(
    session({
      name: COOKIE_NAME,
      store: new RedisStore({
        client: redis,
        disableTouch: true, //optional arg, touching increases the time session will be active
      }),
      cookie: {
        maxAge: 1000 * 60 * 60 * 60 * 366, //1 year cookie time
        httpOnly: true, //javascript code in front end cannot access cookie
        secure: false, //cookie only works in https if true. can set to __prod__ if in prod
        sameSite: "lax", //must be changed to lax for prod
        // domain: __prod__ ? ".yourdomainhere.com" : undefined,
      },
      saveUninitialized: false, //usually false if using express-session
      secret: process.env.SESSION_SECRET as string, //this app does not set cookies, but if it did, this would be needed
      resave: false, //set to false because disable touch is true
    })
  );

  /*****redis middleware ends here*********/

  //App listens on port set in environment variables - here, it is 4000
  app.listen(parseInt(process.env.PORT as string), () => {
    console.log(`🚀 Listening on port ${process.env.PORT}`);
  });
};

main().catch((err) => {
  console.log(err);
});
