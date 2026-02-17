#include <stdio.h>

void stage3(unsigned char *s){
    int i; // [rsp+1Ch] [rbp-4h]

    for ( i = 0; i <= 3; ++i ){
        s[i] ^= 'U';
        printf("%hhx\n", s[i]);
    }
}

void stage2(char *a1){
    int i; // [rsp+14h] [rbp-4h]

    for ( i = 0; i <= 3; ++i )
    {
        a1[i] = a1[i] >> 3 | 32 * a1[i];
    }
    printf("%s\n", a1);
}

void stage1(char *a1){
    int i; // [rsp+1Ch] [rbp-4h]
    for ( i = 0; i <= 3; ++i )
        a1[i] -= 5;
    printf("%s", a1);
}

int main(void){
    unsigned char s[] = "mbmc";
    stage3(s);
    stage2(s);
    stage1(s);

    printf("%s", s);
}
