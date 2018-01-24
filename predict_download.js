const request = require('request')
const csv = require('csv')
const fs = require('fs')
const co = require('co')

// return `${this.domainId}_${this.orgId}_${this.suiteKey}`;
const requestUrl = (mktWord,stockCode) => {
    return new Promise(function(resolve, reject) {
        request(`http://finance.sina.com.cn/realstock/company/${mktWord+stockCode}/houfuquan.js?d=2017-07-14`, function(error, response, body) {
            if (!error && response.statusCode == 200) {} else {
                console.log('connect fail, code !== 200')
                console.log('stock code:'+stockCode)
                return;
            }
            resolve(body)
        })
    })
}
const mapToKV = (rawData) => {
    let arr = []
    let count = 0
    for (let k in rawData) {
        count += 1
        arr.push({date:k,value:rawData[k]})
        // arr.push(rawData[k])
        if (count >= 400) {
            return arr
        }
    }
    return arr
}

function guid() {
    return 'xxxx-xxxx-4xxx-yxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
const save = (content) => {
        const buffer = new Buffer(content)
            //需要转换字符集
            // const iconv = require('iconv-lite')
            // const str = iconv.encode(buffer, 'utf-8')
            // const str = iconv.encode(buffer, 'gb2312');
        fs.writeFileSync('./predictData.json', buffer);
    }
    /*
        上海深圳分开
        未来4周 20个工作日
        倒着算，每次步伐5个工作日
        过去150个工作日 作为输入数据
    */

const truncateAndStr = (data) => {
    let end = data.length-1
    let start = end - 150
    const alreadyCut = data.slice(start, end).map(el=>el.value)
    // console.log(alreadyCut.length)
    return JSON.stringify(alreadyCut)
}
const downloadDataof = (mktWord,stockCode) => {
    co(function*() {
        let body = yield requestUrl(mktWord,stockCode)
        body = body.split('/*')
        body = body[0]
        body = eval(body)
        const rawData = body[0].data
        let data = mapToKV(rawData)
            // const str = JSON.stringify(data)
            // saveToCSV(str)
            // throw new Error('index<=150')

        data.reverse()
        save(truncateAndStr(data))
    })
}

downloadDataof('sh',601318)
