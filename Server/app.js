	var express = require('express');
	var app = express();
	var path = require('path');
	var formidable = require('formidable');
	var fs = require('fs');

	var child;
	var child_cp;
	var child_cp1;
	var exec = require('child_process').exec;
	var cdata=copyData("count.txt","count.txt");
	app.use(express.static(path.join(__dirname, 'public')));
	app.get('/', function(req, res){
		clear(req);
		res.sendFile(path.join(__dirname, 'views/index.html'));
	});
	app.get('/home', function(req, res){
		return res.redirect('/');
	});
	app.post('/upload', function(req, res){
	  //clear(req);
	  cdata = cdata+1;
	  copyData("count.txt","count.txt");
	  var count = parseIP(getClientIp(req));

	  console.log("IP: "+count);
	  child = exec("cd ..;mkdir im"+count+";cd vis;", function(error, stdout, stderr) {
	  // command output is in stdout
	  //console.log(`stdout: ${stdout}`);
	  console.log(`stderr: ${stderr}`);
	  });
	  child.on('exit', function() {
			// create an incoming form object
	  var form = new formidable.IncomingForm();

	  // specify that we want to allow the user to upload multiple files in a single request
	  form.multiples = true;

	  // store all uploads in the /uploads directory
	  form.uploadDir = path.join(__dirname, '../im'+count);

	  // every time a file has been uploaded successfully,
	  // rename it to it's orignal name
	  form.on('file', function(field, file) {
	  	fs.rename(file.path, path.join(form.uploadDir, file.name));
	  });

	  // log any errors that occur
	  form.on('error', function(err) {
	  	console.log('An error has occured: \n' + err);
	  });

	  // once all the files have been uploaded, send a response to the client
	  form.on('end', function() {

	  	res.send({redirect: '/result'});
	 	//getCalled(req,res,null);
	    //res.end('success');
	});

	  // parse the incoming request containing the form data
	  form.parse(req);
	});
	  

	});
	app.get('/result',createModel);

	function clear(req){
		var count = parseIP(getClientIp(req));
		child = exec("rm -rf imgs/*", function(error, stdout, stderr) {
	  // command output is in stdout
	  //console.log(`stdout: ${stdout}`);
	  console.log(`stderr: ${stderr}`);
	});
		child = exec("rm -rf public/imgs/*", function(error, stdout, stderr) {
	  // command output is in stdout
	  //console.log(`stdout: ${stdout}`);
	  console.log(`stderr: ${stderr}`);
	});
		child = exec("rm -rf ../im"+count+"/*", function(error, stdout, stderr) {
	  // command output is in stdout
	  //console.log(`stdout: ${stdout}`);
	  console.log(`stderr: ${stderr}`);
	});
	}

	function createModel(req, res, obj){
		var count = parseIP(getClientIp(req));

		var image_folder = "im"+count
		child = exec("cd ..;th eval.lua -model model_id1-501-1448236541.t7_cpu.t7 -image_folder "+image_folder+" -num_images 10 -gpuid -1;cd vis;", function(error, stdout, stderr) {
	  // command output is in stdout
	  console.log("th eval.lua -model model_id1-501-1448236541.t7_cpu.t7 -image_folder "+image_folder+" -num_images 10 -gpuid -1;");
	  console.log(`stderr: ${stderr}`);
	});
		child.on('exit', function() {
			child = exec("mkdir public/"+image_folder, function(error, stdout, stderr) {
	  // command output is in stdout
	  //console.log(`stdout: ${stdout}`);
	  console.log(`stderr: ${stderr}`);
	});
			child_cp =exec("cp -r "+image_folder+"/vis.json public/"+image_folder+"/vis.json", function(error, stdout, stderr) {
	  // command output is in stdout
	  console.log(`stdout: file copied`);
	  console.log(`stderr: ${stderr}`);
	});
			child_cp.on('exit', function() {
				child_cp1 = exec("cp -r "+image_folder+"/* public/"+image_folder+"/", function(error, stdout, stderr) {
	  		// command output is in stdout
	  		console.log(`stdout: images file copied`);
	  		console.log(`stderr: ${stderr}`);
	  		console.log('now redirecting');  
	  		return res.sendFile(path.join(__dirname+'/views/result.html'));
	  	});
			})
		})

	}
	app.get("/getvar", function(req, res){
		//var count = parseIP(getClientIp(req));
	     console.log("server getvar");

		var strings = parseIP(getClientIp(req));
		console.log(getClientIp(req));
		console.log(strings);
		res.send(strings)
		// res.json({ count: count });
	});

	app.get("/getcount", function(req, res){
		//var count = parseIP(getClientIp(req));
	     console.log("server getvar");

		//var strings = copyData("count.txt","count.txt");
		//console.log(strings);
		res.send(cdata.toString())
		// res.json({ count: count });
	});


	function getClientIp(req) {
		var ipAddress;
	  // The request may be forwarded from local web server.
	  var forwardedIpsStr = req.header('x-forwarded-for'); 
	  if (forwardedIpsStr) {
	    // 'x-forwarded-for' header may return multiple IP addresses in
	    // the format: "client IP, proxy 1 IP, proxy 2 IP" so take the
	    // the first one
	    var forwardedIps = forwardedIpsStr.split(',');
	    ipAddress = forwardedIps[0];
	}
	if (!ipAddress) {
	    // If request was not forwarded
	    ipAddress = req.connection.remoteAddress;
	}
	return ipAddress;
	};

	function parseIP(ip) {
		console.log("ip: "+ip);
		var res0 = ip.split(":");

		if(res0.length<4){
			return "local";
		}
		else{
			var res1 = res0[3].split(".");
			var res2="";
			for(var i=0;i<res1.length;i++){
				res2=res2+res1[i];
			}
			return res2;
		}
	};

	function copyData(savPath, srcPath,callback) {
    fs.readFile(srcPath, 'utf8', function (err, data) {
            if (err) throw err;
            //Do your processing, MD5, send a satellite to the moon, etc.
            cdata = parseInt(data);
            console.log(data);
            cdata=cdata+1;
            console.log(cdata);

            fs.writeFile (savPath, cdata, function(err) {
                if (err) throw err;
                console.log('complete');
            });
        });
    return cdata;
	}

	var server = app.listen(8000);
