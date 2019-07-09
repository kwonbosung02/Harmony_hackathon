from gtts import gTTS
import os
tts = gTTS(text='사진 찍습니다. 하나...... 둘...... 셋', lang='ko')
tts.save("music3.mp3")
