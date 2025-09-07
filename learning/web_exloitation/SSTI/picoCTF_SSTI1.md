# picoCTF SSTI1

## Description
I made a cool website where you can announce whatever you want! Try it out!  
I heard templating is a cool and modular way to build web apps! Check out my website [here](http://rescued-float.picoctf.net:53557/)!

### Thoughts
This was my first time looking at a web exploitation question so I searched up SSTI and found that it stands for Server Side Template Injection.  

This lead me down the rabbit hole of learning and understanding what SSTI is and how I can exploit its vulnerabilities.  

I will be releasing a writeup on SSTI after gaining more experiences on using it.

### Process
Once I understood this is on SSTI, I tried several inputs to test which template is being used:

> ${7*7}  

Which caused the page to return ${7*7}, this tells me that it is not **Mako** or some unknown template.  
Next I tried:

> {{7*7}}

Which gave me **49**, so that tells me that the code I gave is executing inside the template. To test and narrow down even further, I tried:

> {{7*'7'}}

Which gave me **7777777**, so the template being used is **Jinja2**. If it were to output 49, then the template used would be Twig.  

Jinja2 is a template engine that allows writing code similar to python syntax. So we can do some shennanigans!

> {{self}}  
> {{config}}  
> {{request}}

Lets go through what each of these do and why I am trying to achieve and understand.  

Generally in SSTI, we want to find a way to read sensitive data. 

> {{self}} outputs TemplateReference None 

This tells me that Jinja2 is executing my malicious code