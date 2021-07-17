# https://github.com/shawwwn/uMail

import user_lib.umail as umail

smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
smtp.login('yanco54321@gmail.com', 'thePassword')
smtp.to('yaniv.choen.1@gmail.com')
smtp.write("From: yan <yanco54321@gmail.com>\n")
smtp.write("To: Alice <yaniv.choen.1@gmail.com>\n")
smtp.write("Subject: this is a test subject\n\n")
smtp.write("first line test.\n")
smtp.write("secend line test.\n")
smtp.write("...\n")
smtp.send()
smtp.quit()