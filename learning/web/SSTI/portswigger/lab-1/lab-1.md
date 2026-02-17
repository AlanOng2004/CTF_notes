# Lab: Basic server-side template injection

[This lab](https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic) is vulnerable to server-side template injection due to the unsafe construction of an ERB template.

To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.


## Attempting the challenge

![website picture](website.png)

When clickingon the caution sign product, I get "Unfortunately this product is out of stock". The other products lead me to the product page itself so I determine that this is where the template injection must occur.

![looking into the html](htmlpic.png)

So from the challenge description, I know that this website was made from [ERB template](https://docs.ruby-lang.org/en/2.3.0/ERB.html). I also need to find out how to execute arbitrary code.

[How to do template injection in Ruby?](https://github.com/appsecengineer/ruby-ssti)

Reading this didn't get me anywhere as I am unable to find the ruby file attached to this website.

So I did a quick read through of the solutions, but alas my problem was finding the ruby file and not really with the template injection. Finally I gave up and watched a [youtube video](https://www.youtube.com/watch?v=QLqHMMcBXuQ&t=31s).

The guy uses Burp Suite Professional to look at the website.