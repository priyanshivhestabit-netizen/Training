const fs = require("fs");

const metrics = {
	cpuUsage: process.cpuUsage(),
	resourceUsage: process.resourceUsage(),
};

fs.writeFileSync(
	"./logs/day1-symmetrics.json",
	JSON.stringify(metrics,null,2)
);

console.log("System metrics stored in the file");
