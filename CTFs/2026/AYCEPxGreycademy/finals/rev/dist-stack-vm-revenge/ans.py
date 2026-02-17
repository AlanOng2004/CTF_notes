def run_vm(instructions, user_input):
    stack = []
    ans = []

    take = True
    instr = ""
    result = ""

    for insn in instructions.split('\n'):        

        parts = insn.split(' ')
        opcode = parts[0]
        if opcode == 'push' and take:
            val = int(parts[1])
            stack.append(val)

        elif opcode == 'input':
            take = True

        elif opcode == 'add' and take:
            instr = "add"

        elif opcode == 'xor' and take:
            instr = "xor"

        elif opcode == 'sub' and take:
            instr = "sub"

        elif opcode == 'equal' and take:
            take = False
            if instr == "add":
                b = stack.pop()
                a = stack.pop()
                ans.append(chr(b-a))
            if instr == "sub":
                b = stack.pop()
                a = stack.pop()
                ans.append(chr(b+a))
            if instr == "xor":
                b = stack.pop()
                a = stack.pop()
                ans.append(chr(b^a))


        elif opcode == 'swapswap':
            if len(stack) < 2:
                continue

    for i in ans:
        result += i
    print(result)
    return result 



if __name__ == '__main__':
    # tip: there's a lot of redundant instructions, how do we filter them out?
  with open('instructions_revenge.txt', 'r') as f:
      instructions = f.read()

  user_input = input('Enter your flag: ')
  result = run_vm(instructions, user_input)
  print(result)

  if result:
      print('\n🎉 Correct! Flag validated successfully!')
  else:
      print('\n❌ Wrong flag. Try again!')

