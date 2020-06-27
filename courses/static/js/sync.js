var req = new XMLHttpRequest()

req.open('GET', '/api/?command=validate')
req.send()
 

function midnight() {
    var date = new Date()
    var hour = date.getHours()
    var minute = date.getMinutes()
    var second = date.getSeconds()

    if (hour === 0){
        if (minute === 0){
            if (second === 0){
                return true
            }
        }
    }
    return false
}