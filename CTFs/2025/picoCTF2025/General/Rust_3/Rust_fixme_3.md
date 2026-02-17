# Rust fixme 3

Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag!
Download the Rust code [here](https://challenge-files.picoctf.net/c_verbal_sleep/dcdaf491b35c1d0f5075e9583edbbb7aaea1dffb6ad32bc000e4d87b5200ff7b/fixme3.tar.gz).

Given Documenatation of [unsafe rust](https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html).

## Attempt

So we learn that if we want to declare an unsafe function, we need to add

> unsafe {  
>   function   
>}

![pic1](pics/pic1.png)

So yea we are using an unsafe function without declaring it, which is why the cargo check is screaming at us.

![pic2](pics/pic2.png)

And now we run the code and get the flag!