Redacted 

Description
wait, i thought XORing something with itself gives all 0s??

65 6c ce 6b c1 75 61 7e 53 
66
c9 52 d8 6c
6a
53 6e 6e de
52 df 63 6d 7e 75 7f ce 64 d5 63 73

from hex gives me:
elÎkÁua~SfÉRØljSnnÞRßcm~u


Using cyberchef to reverse the steps, I used From Hex and XOR
using the output i got from From Hex as the key

I get kfÁgÌyot\jÄ^Öfe_cbÐXÐo`r{uÁhØo}

Rotating it right by 1 gets me µ3à³f¼·:.5b/k3²¯±1h,h·09½ºà4l·¾

this method is wrong


trying again i noted that:
cipher = plaintext xor key
plaintext = cipher xor key
key = plaintext xor cipher

therefore i need to find the key by using the cipher and plaintext, i have the first few lines of the plaintext ictf{
which equates to 

69 63 74 66 7b

so trying to xor it will give me 
SUî]òE[úK÷SLù	

now i unhex the given cipher and xor with the key which gives me:
kbÀeÏ{op]hÇ\Öbd]``Ð\Ñmcp{qÀjÛm}

its hex is 
6b 62 c0 65 cf 7b 6f 70 5d 68 c7 5c d6 62 64 5d 60 60 d0 5c d1 6d 63 70 7b 71 c0 6a db 6d 7d

so xoring it with 

this also does not work

