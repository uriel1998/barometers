Pipe to `aha` > out.html  
cutycapt --url=file:///home/steven/documents/programming/barometer_map/out.html --out=cutycapt.png

https://youtu.be/jebfz7ZmBoc


https://asciinema.org/a/hzEo7IleqUtRVjHYFyCdV9sAE
https://github.com/asciinema/asciinema-player/releases
<html>
<head>
  <link rel="stylesheet" type="text/css" href="/asciinema-player.css" />
</head>
<body>
  <asciinema-player src="/455653.cast" cols="126" rows="69"></asciinema-player>
  ...
  <script src="/asciinema-player.js"></script>
</body>
</html>


https://www.xmodulo.com/convert-html-web-page-png-image-linux.html

While CutyCapt is a CLI tool, it requires an X server running. If you attempt to run CutyCapt on a headless server, you will get the error:

cutycapt: cannot connect to X server :0

If you want to run CutyCapt on a headless server without X windows, you can set up Xvfb (lightweight fake X11 server) on the server, so that CutyCapt does not complain.

To install Xvfb on Debian, Ubuntu or Linux Mint:

$ sudo apt-get install xvfb

To install Xvfb on Fedora, CentOS or RHEL:

$ sudo yum install xvfb

After installing Xvfb, proceed to run CutyCapt as follows.

$ xvfb-run --server-args="-screen 0, 1280x1200x24" cutycapt --url=http://www.cnn.com --out=cnn.png

It will launch Xvfb server first, and then use CutyCapt to screen capture the webpage. So it may take longer. If you want to make multiple screenshots, you may want to start Xvfb server as a background daemon beforehand.
