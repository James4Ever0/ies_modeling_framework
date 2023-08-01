var md = require('markdown-it')(),
    mathjax3 = require('markdown-it-mathjax3');

md.use(mathjax3);

// double backslash is required for javascript strings, but not html input
const {writeFileSync, readFileSync} = require("fs");

var input = readFileSync("jump_to_line.md", {'encoding': 'utf8','mode':'r'});
var result = md.render(input);

writeFileSync("jump_to_line.html", result)