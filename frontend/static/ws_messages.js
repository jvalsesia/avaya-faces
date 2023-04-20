var ip = location.hostname;
var socket = io("https://" + ip + ":5500");
socket.on('connect', function () {
    socket.emit('my event', { data: 'I\'m connected!' });
});

socket.on('recognized', function (userName) {
    document.getElementById("recognized_userName").innerHTML = JSON.stringify(userName);
    console.log(userName);
});