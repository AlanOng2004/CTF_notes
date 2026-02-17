# pyjail

Can you escape the jail?

nc pyjail.challs.infobahnc.tf 1337

## Recon

```
import io
import contextlib

with open("flag.txt", 'rb') as f:
    FLAG = f.read()

def run(code):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(code, {})
    except Exception:
        return None
    return buf.getvalue() or None

code = input("Enter your solution: ")

if len(code) > 15:
    print("Code too long")
    exit()

if not set(code) <= set("abcdefghijklmnopqrstuvwxyz "):
    print("Invalid characters")
    exit()

result = run(code)

if result is None:
    print("Error")
    exit()

if len(result) > 500:
    print(FLAG)
else:
    print("Output too short")
```

When we run `nc pyjail.challs.infobahnc.tf 1337`, we are prompted with an input. 

Looking at the source code, we see that the conditions for the input to give us the flag are:
1. input length <= 15
2. the characters have to be in this set: "abcdefghijklmnopqrstuvwxyz "
3. run(input) needs to output a result with length > 500

In run(code) we see `exec(code, {})`

`exec(source, globals)` executes source using the provided globals mapping as the global namespace. If you only pass two args, locals defaults to the same mapping as globals.

When an empty dict {} is passed into the globals parameter, Python will insert a `__builtins__` entry into that dict (unless you explicitly provide one). That gives the executed code access to builtins (e.g. print, len, `__import__`, etc.).

### Python Easter Egg
When python executes `import this`, the module’s top-level code prints The Zen of Python (a short poem). That text is well over 500 characters. So exec("import this", {}) produces stdout whose length exceeds 500, which triggers the sandbox to print the flag.

We can therefore use `import this` as a payload and get the flag.

## Attempt
```
nc pyjail.challs.infobahnc.tf 1337
== proof-of-work: disabled ==
Enter your solution: import this
b'infobahn{Y0u_3Sc4p3D_Th3_J@1lll_4359849084894}\n'
```

