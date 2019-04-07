import os
import speech_recognition as sr
dir_path = os.path.dirname(os.path.realpath(__file__))

#r = sr.Recognizer()
#mic = sr.Microphone()
#egg, apple, banana, carrot, orange, bread
#shirt, pants, sweater, socks, hat, shoes
#blanket, tissues, comb, chapstick, bottle, backpack 
#thingsWeGive = ["blanket", "blankets", "tissues", "comb", "chapstick", "bottle", "bottles", "backpack", "backpacks", "shirt", "shirts", "pants","hat", "hats", "shoes", "socks", "sweater", "sweaters", "apple", "apples", "banana", "bananas", "carrot", "carrots", "egg", "eggs", "orange", "oranges", "bread"]
#numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "one", "two", "too", "to", "three", "tree", "four", "for", "five", "six", "seven", "eight", "nine", "ten"]
#thingsTheyNeed = []
 hellow = sr.AudioFile(dirpath + '\\uploads\\temp.wav')
 with hellow as source:
    audio = r.record(source)
s = r.recognize_google(audio)
#print("Text: " + s)

"""
with mic as source:
     r.adjust_for_ambient_noise(source)
     audio = r.listen(source)


def listen(r,mic):
        try:
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=20, phrase_time_limit=None)
            return r.recognize_google(audio)
        except speech_recognition.WaitTimeoutError:
           return "I could not hear you!"
        except speech_recognition.UnknownValueError:
            return "I did not quite get that"
        except speech_recognition.RequestErrro as e:
            return "Recognition Error: {0}".format(e) 
print("start")


out = listen(r, mic)


for i in range(len(out)):
	if(out[i] in thingsWeGive):
		if(out[i-1] in numbers):
			thingsTheyNeed.append(out[i-1])
		thingsTheyNeed.append(out[i])


print(thingsTheyNeed)
"""
#35.188.226.236
#35.245.40.128
_url = http://domain.com.domain.com.com/post_req
_params = {
id: [id]
text: [s]
addressed: false
user: ''
}

res = requests.post(url = _url, params = _params)
