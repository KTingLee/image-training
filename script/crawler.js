const fs = require('fs')
const fetch = require('node-fetch')

const sleep = function (t) {
  return new Promise(function (resolve, reject) {
    setTimeout(function () {
      resolve()
    }, t)
  })
}

const url = `https://bsr.twse.com.tw/bshtm/`

;(async () => {
  await downloadImages(10, 16)
})()

async function downloadImages (number, firstId = 0) {
  for (let i = firstId; i < number+firstId; i++) {
    let res = await fetch(`${url}bsMenu.aspx`)
    res = await res.text()
  
    const imageUrl = url + /CaptchaImage\S+/.exec(res)[0].replace(`'`, ``)
    res = await fetch(imageUrl)
    res = await res.buffer()
    await sleep(1000)
    fs.writeFileSync(`../captcha_Images/${i}.png`, res, 'binary')
  }
}
