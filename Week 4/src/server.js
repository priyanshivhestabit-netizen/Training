const {loadEnv} = require("./config/loaders/env.loader");
const connectDB=require("./loaders/db");
const loadApp = require("./loaders/app");
const logger =require("./utils/logger");

async function startServer(){
    loadEnv();

    await connectDB();

    const app = loadApp();

    const PORT=process.env.PORT || 3000;
    const server = app.listen(PORT,()=>{
        logger.info(`Server started on port ${PORT}`);
    });

    //graceful shutdown
    process.on("SIGINT",()=>{
        logger.info("Shutting down server!");
        server.close(()=>{
            process.exit(0);
        });
    });

}

startServer();