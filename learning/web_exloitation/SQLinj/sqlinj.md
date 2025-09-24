# SQL INJECTION

[Cheatsheet](https://portswigger.net/web-security/sql-injection/cheat-sheet) by PortSwigger

Learnt using:
1. [Portswigger](https://portswigger.net/web-security/sql-injection)

## Ways to detect SQL injection vulnerabilities

We will usually use these methods to check if there is any SQL injection vulnerabilities. We try them against every entry point of the application.

1. Using single quote `'` and look for any errors or anomalies
2. Boolean conditions like `OR 1=1` or `OR 1=2`


## Retrieving Hidden Data

Given the original link, `https://insecure-website.com/products?category=Gifts`, we see that there is an SQL query. 

> SELECT * FROM products WHERE category = 'Gifts' AND released = 1

We can exploit that by commenting out the `AND released = 1` part.

>https://insecure-website.com/products?category=Gifts'-- 

If we wanted to retrieve everything from the database, we can use a boolean condition like this:

> https://insecure-website.com/products?category=Gifts'+OR+1=1--

