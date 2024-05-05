from math import gcd
import PySimpleGUI as sg

sg.theme('Dark Blue 12')

def lcm(p, q):
    #最小公倍数
    return (p*q) // gcd(p, q)

def gen_key(p, q):
    N = p * q
    L = lcm(p - 1, q - 1)
    for i in range (2, L):
        if gcd(i, L) == 1:
            E = i
            break
    
    for i in range (2, L):
        if (E * i) % L == 1:
            D = i
            break
    
    return (E, N), (D, N)

def encrypt(text, public_key):
    #暗号化
    E, N = public_key
    text_integers = [ord(char) for char in text]
    encrypt_integer = [pow(i, E, N) for i in text_integers]
    en_int_bin = [format(i, 'b') for i in encrypt_integer]  #2進数化!
    mapL = map(str, en_int_bin)                             #joinできる形に!
    encrypted_text = ' '.join(mapL)
    return encrypted_text

def decrypt(en_text, private_key):
    #復号
    D, N = private_key
    true_en_text = en_text.split()
    en_text = [int(i, 2) for i in true_en_text]
    decrypt_integer = [pow(i, D, N) for i in en_text]
    decrypted_text = ''.join(chr(i) for i in decrypt_integer)
    return decrypted_text

#def sanitize(en_text):
    #return en_text.encode('utf-8', 'replace').decode('utf-8')

frameEn = [
    [[sg.Text('平文')], [sg.InputText(key='UserEnText')]],
    [[sg.Text('素数A')], sg.InputText(default_text='101', key='UserP')],
    [[sg.Text('素数B')], sg.InputText(default_text='281', key='UserQ')],
    [sg.Checkbox('確認ポップアップを表示',key='DeToggle' ,default=True)],
    [sg.Button('暗号化', key='DoEn')]
]

frameDe = [
    [[sg.Text('暗号文')], sg.InputText(key='UserDeText')],
    [[sg.Text('鍵d')], sg.InputText(key='UserD')],
    [[sg.Text('鍵N')], sg.InputText(key='UserN')],
    [sg.Button('復号', key='DoDe')]
]

layout = [
    [[sg.Text('暗号化')], [frameEn]],
    [[sg.Text('復号')], [frameDe]],
    [sg.Output(size=(80, 20))],
    [sg.Submit('終了')]
]

window = sg.Window('文章暗号化&復号', layout, no_titlebar=True, grab_anywhere=True)

while True:
    event, values = window.read()
    if event is None:
        break

    if event == 'DoEn':
        #暗号化
        pub_key, priva_key = gen_key(int(values['UserP']), int(values['UserQ']))
        popToggle = values['DeToggle']
        text = values['UserEnText']
        en_text = encrypt(text, pub_key)
        KeyPop = "公開鍵eN:" + str(pub_key) + '\n'
        KeyPop += "秘密鍵dN:" + str(priva_key) + "\n"
        KeyPop += "鍵は絶対に忘れないでください!!"
        if popToggle:
            sg.popup(KeyPop, title='完了しました!')
        #sg.Print('暗号化完了', text_color='white', background_color='blue')
        print(f'''平文　: {text}\n公開鍵eN: {pub_key}\n秘密鍵dN: {priva_key}\n暗号文:\n{en_text}\n''')
    
    if event == 'DoDe':
        #復号
        Dekey = (int(values['UserD']), int(values['UserN']))
        DeText = values['UserDeText']
        de_text = decrypt(DeText, Dekey)
        #sg.Print('復号完了', text_color='white', background_color='red')
        print(f'''使用鍵dN: {Dekey}\n復号文: {de_text}\n''')
    
    if event == '終了':
        break

window.close()