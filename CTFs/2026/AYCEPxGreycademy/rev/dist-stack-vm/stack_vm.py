def run_vm(instructions, user_input):
    stack = []
    input_bytes = [ord(c) for c in user_input]

    for insn in instructions.split('\n'):        
        parts = insn.split(' ')
        opcode = parts[0]

        if opcode == 'push': #pushes the instruction num onto stack 
            val = int(parts[1])
            stack.append(val)

        elif opcode == 'input': #pushes ord(flag[i] onto stack)
            idx = int(parts[1])
            if idx >= len(input_bytes):
                return False
            stack.append(input_bytes[idx])

        elif opcode == 'add': #adds the top 2 stack nums
            if len(stack) < 2:
                return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)

        elif opcode == 'xor': #xor the top 2 stack nums
            if len(stack) < 2:
                return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a ^ b)

        elif opcode == 'sub': #subs the top 2 sub num
            if len(stack) < 2:
                return False
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)

        elif opcode == 'equal': #if equal continue
            if len(stack) < 2:
                return False
            b = stack.pop()
            a = stack.pop()
            if a != b:
                return False

    return True


if __name__ == '__main__':
    with open('instructions.txt', 'r') as f:
        instructions = f.read()

    user_input = input('Enter your flag: ')
    result = run_vm(instructions, user_input)

    if result:
        print('\n🎉 Correct! Flag validated successfully!')
    else:
        print('\n❌ Wrong flag. Try again!')
