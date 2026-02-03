const os = require("os");
const { execSync } = require("child_process");

//hostname
console.log("Hostname:",os.hostname());

//disk space(GB)
try{
	const disk = execSync("df -h --total | grep total").toString();
	console.log("Disk space:", disk);
}
catch(e){
	console.log("Disk info not available");
} 

//open ports(top 5)
try{
	const ports = execSync("ss -tuln | head -n 6").toString();
	console.log("Open Ports:\n",ports);
}
catch(e){
	console.log("Ports info not available");
}

//default gateway

try{
	let gateway;
	try{
		gateway = execSync(
			"ip route | awk '/default/{print $3}'"
		).toString().trim();
	}
	catch{
		gateway  = execSync(
			"route -n | awk '$1 == \"0.0.0.0\" {print $2}'"
		).toString().trim();
	}
	if(!gateway) throw new Error("No gateway");
	
	console.log("gateway:",gateway);
}
catch(e){
	console.log("gateway info not found");
}
//logged-in users
let loggedInUsers = "N/A";
try{
	const users = execSync("who | wc -l");
	loggedInUsers = parseInt(users, 10);

	console.log("Logged-in users:",loggedInUsers);
}
catch(e){
	console.log("Users info not available");
}
