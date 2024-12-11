const axios = require("axios") //для тех кто забыл npm i cheerio
const cheerio = require("cheerio")// npm i axios
    axios.get("http://localhost/test1/index.php").then(html =>{
        const tag = cheerio.load(html.data)
        let text = ""
        tag("body:nth-child(2) > p:nth-child(1)").each((i, elem) =>{
            text += `${tag(elem).text()}\n`
        })
        console.log(text);
        console.log("Hello");
    })