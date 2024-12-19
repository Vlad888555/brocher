const axios = require("axios") //для тех кто забыл npm i cheerio
const cheerio = require("cheerio")// npm i axios
    axios.get("https://q-parser.ru").then(html =>{
        const tag = cheerio.load(html.data)
        let text = ""
        tag("body > div:nth-child(1) > main > div.container.flex.flex-col.gap-8.px-4.py-16 > div.flex.flex-col.max-w-3xl.gap-8.mx-auto > h1").each((i, elem) =>{
            text += `${tag(elem).text()}\n`
        })
        console.log(text);
        console.log("Hello");
    })