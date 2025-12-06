const axios = require('axios'); // import thu vien để gọi
const lodash = require('lodash'); // import thư viện lodash để xử lý những hàm như cắt chuỗi, tính toán hay là những hàm rút gọn cần dùng
const { appRun, appKill, appState, appInfo, usleep, touchDown, touchUp, touchMove, inputText, screenshot, toast, keyDown, keyUp } = at // import những key mà mình hay xài để không cần khai at.

function demo() {
    changeStatus("Open Facebook")
    appRun("com.facebook.Facebook")
    usleep(5000000);
    changeStatus("Click Mobile number or email")
    clickToText("Mobile number or email")
    usleep(2000000);
    changeStatus("Get Mail")
    for(i=0;i < 30;i++) {
        mail = checkFileMail()
        usleep(2000000);
    }
    changeStatus("Click Password")
    clickToText("Password")
    usleep(2000000);
    appKill("com.facebook.Facebook")
    changeStatus("Complete")
}

function clickToText(textReg) {
    at.findText({}, text => text === textReg, (result, error) => {
        if (error) {
            alert('Failed to findText, error: %s', error)
            return
        }
        console.log('Got result by findText asynchronously', result);

        if (result.length > 0) {
            usleep(84627.58);
            touchDown(3, result[0]["bottomRight"]["x"], result[0]["bottomRight"]["y"]);
            usleep(84627.58);
            touchUp(3, result[0]["bottomRight"]["x"], result[0]["bottomRight"]["y"]);
            usleep(84627.58);
            isFindout = true
        }
    })
    usleep(1000000);
}
function changeStatus(statusText) {
    const [exists, isDir] = fs.exists('/var/mobile/Library/AutoTouch/Scripts/status.txt')
    if (exists === false) {
        const [done, error] = fs.writeFile('/var/mobile/Library/AutoTouch/Scripts/status.txt', statusText)
    } else {
        const [done, error] = fs.writeFile('/var/mobile/Library/AutoTouch/Scripts/status.txt', statusText, true)
    }
}

function checkFileMail() {
    const [exists, isDir] = fs.exists('/var/mobile/Library/AutoTouch/Scripts/mail.txt')
    if (exists === true) {
        const [content, error] = fs.readFile('/var/mobile/Library/AutoTouch/Scripts/mail.txt')
        if (content === "") {
            return ""
        } else {
            return content
        }
    } else {
        return ""
    }
}

function startProcess(email, password, month_birthday) {
    // Viết Script vào để chạy
}


function start() {
    const [content, error] = fs.readFile('/var/mobile/Library/AutoTouch/Scripts/config.json', 'utf8')
    const email = JSON.parse(content)['email']
    const password = JSON.parse(content)['password']
    const month_birthday = JSON.parse(content)['month_birthday']

    startProcess(email, password, month_birthday)
}

start()