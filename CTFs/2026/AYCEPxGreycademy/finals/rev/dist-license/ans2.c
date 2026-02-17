_BOOL8 __fastcall stage3(const char *a1)
{
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 3; ++i )
    a1[i] ^= 'U';
  return strcmp(a1, "mbmc") == 0;
}

__int64 __fastcall stage2(__int64 a1)
{
  int i; // [rsp+14h] [rbp-4h]

  for ( i = 0; i <= 3; ++i )
  {
    *(_BYTE *)(i + a1) = (*(_BYTE *)(i + a1) >> 3) | (32 * *(_BYTE *)(i + a1));
    if ( *(_BYTE *)(i + a1) != expect_0[i] )
      return 0;
  }
  return 1;
}

_BOOL8 __fastcall stage1(const char *a1)
{
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 3; ++i )
    a1[i] -= 5;
  return strcmp(a1, "1142") == 0;               // if (a1 != 1142) return 1
}

_BOOL8 __fastcall validate_license(__int64 a1)
{
  char v2[5]; // [rsp+19h] [rbp-17h] BYREF
  _BYTE v3[5]; // [rsp+1Eh] [rbp-12h] BYREF
  _BYTE v4[5]; // [rsp+23h] [rbp-Dh] BYREF
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  if ( (unsigned int)__isoc99_sscanf(a1, "%4[0-9]-%4[0-9]-%4[0-9]%n") != 3 )
    return 0;
  return stage1(v2) && (unsigned int)stage2(v3) && (unsigned int)stage3(v4);
}

int __fastcall main(int argc, const char **argv, const char **envp)
{
  char s[40]; // [rsp+0h] [rbp-30h] BYREF
  unsigned __int64 v5; // [rsp+28h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  printf("Enter License: ");
  fgets(s, 25, stdin);
  s[strcspn(s, "\n")] = 0;
  if ( strlen(s) == 14 && validate_license((__int64)s) )
    printf("Congrats! The flag is grey{%s}\n", s);
  else
    puts("Wrong!");
  return 0;
}


