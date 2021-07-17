# https://github.com/shawwwn/uMail

import user_lib.umail as umail

smtp = umail.SMTP('smtp.gmail.com', 587, username='yanco54321@gmail.com', password='thePassword')
smtp.to('yaniv.choen.1@gmail.com')
smtp.send("This is an example.")
smtp.quit()