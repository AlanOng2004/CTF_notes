dict = {
	
}

text = "THIS IS DRIVING ME INSAAAANNNNEEEEEEEEEEEEEE"

for character in text:
	if character not in dict:
		dict[character] = 1
	else:
		dict[character] += 1

print(dict)

for count in dict.keys():
        print(chr(dict[count] + 64))
