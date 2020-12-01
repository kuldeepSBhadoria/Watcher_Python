import time
import nexmo
# Import smtplib for the actual sending function
import smtplib, ssl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the email modules we'll need
from email.message import *
s="k"
message = ""
FILE_TO_WATCH = "/root/LINUX/hotplug/nohup.out"

class Watcher:
    DIRECTORY_TO_WATCH = "/root/LINUX/hotplug"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "..Exit.."

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        w = Watcher()
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "Received created event - %s." % event.src_path
            s = event.src_path
	   # if s.find("sunvts.err"):
	    #   print "detected"
               #mail()			
	     #  message()
        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print "Received modified event - %s." % event.src_path
            s = event.src_path
	    with open(FILE_TO_WATCH) as myfile:
	      	 content = myfile.read()
	         print(content)
                 if 'link speed is not X4' in content:	
					print "link speed is not X4"
					myfile.seek(0, 0) 
			#message(2)
                 elif 'Drive is missing' in content:	
					print "Drive missed real failure" 
					myfile.seek(0, 0) 
					message(1)

def mail():
	gmail_user = '123ssd.samsung@gmail.com'  
	gmail_password = '....'

	sent_from = gmail_user  
	to = ['kuldeepbhadoriaxx@gmail.com','kxxxbhadxxoria@samsung.com']  
	subject = 'OMG Super Important Message'  
	body = 'Hey, what'

	email_text = "kuldeep"

	try:  
	    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	    server.ehlo()
	    server.login(gmail_user, gmail_password)
	    server.sendmail(sent_from, to, email_text)
	    server.close()

	    print 'Email sent!'
	except:  
	    print 'Something went wrong...'

def message(i):
	client = nexmo.Client(key='5ef03909', secret='omiBgsZg5cljMQoT')
	if(i == 1):
		client.send_message({ 'from': '18622296358',   'to': '16504479401',   'text': 'X7-3 Drive missing',})
	elif(i == 2):
		client.send_message({ 'from': '18622296358',   'to': '16504479401',   'text': 'X7-3 Drive Link speed ..',})

if __name__ == '__main__':
    w = Watcher()
    w.run()
