//main.js


const electron = require('electron')
const {app, BrowserWindow} = electron

//frame
app.on('ready', () => {
	let win = new BrowserWindow({
		width:1400,
		height:800,
	})

	//let child = new BrowserWindow
  win.setMenu(null);
	win.loadURL('file://'+__dirname+'./html5up-hyperspace/index.html')

  win.on('closed', () => {
    // 윈도우 객체의 참조를 삭제합니다. 보통 멀티 윈도우 지원을 위해
    // 윈도우 객체를 배열에 저장하는 경우가 있는데 이 경우
    // 해당하는 모든 윈도우 객체의 참조를 삭제해 주어야 합니다.
    win = null
  })
  //let contents = win.webContents
  //contents.startdrag()
})

app.on('closed', () => {
  // 윈도우 객체의 참조를 삭제합니다. 보통 멀티 윈도우 지원을 위해
  // 윈도우 객체를 배열에 저장하는 경우가 있는데 이 경우
  // 해당하는 모든 윈도우 객체의 참조를 삭제해 주어야 합니다.
  app = null
})

