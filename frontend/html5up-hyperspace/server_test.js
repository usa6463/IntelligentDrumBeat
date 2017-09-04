var io = require('socket.io').listen(80);  // 80 포트로 소켓을 엽니다
 
io.sockets.on('connection', function (socket) { // connection이 발생할 때 핸들러를 실행합니다.
	console.log('server running at 80 port');
	socket.emit('news', { hello: 'world' }); // 클라이언트로 news 이벤트를 보냅니다. (hello 라는 키에 world라는 값이 담깁니다)

	socket.on('my other event', function (data) { // 클라이언트에서 my other event가 발생하면 데이터를 받습니다.
		console.log(data);
	});
});