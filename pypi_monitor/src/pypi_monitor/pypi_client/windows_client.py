import requests
import time
import threading

#main data client class 
class DataClient():
    def __init__(self, main_window):
        self.main_window = main_window
        self.queue = DataQueue(self.main_window)

#queue for grabbing incoming data
class DataQueue():
    def __init__(self, main_window):
        #init loop and start it
        self.main_window = main_window
        self.main_window.data = {}
        self.update_request_settings()
        self.start_request_loop()
    
        #function that can be called anytime a settings change was accepted in the IPDialog in gui_settings.py
    def update_request_settings(self):
        #update to new settings and reconstruct the url for the get request
        self.update_rate = int(self.main_window.settings["update_rate"])
        self.ip = self.main_window.settings["ip"]
        self.port = self.main_window.settings["port"]
        self.is_running = self.main_window.settings["is_running"]
        self.url = "http://" + self.ip + ":" + self.port + "/api/rootnode"
    
    #function for starting a data_request() loop in a thread so that gui_main.py is able to continue executing past when this is called
    def start_request_loop(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.data_request, daemon=True) #daemon thread so it dies when the script that started it (gui_main.py) dies
        self.thread.start()

    #function to stop the data_request() loop thread
    def stop_request_loop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(5) # wait for the thread to finish with a 5 second timeout

    #main loop that will send out the https requests to cather data 
    def data_request(self):
        while self.is_running:
            try:
                self.main_window.data = requests.get(self.url)
                print(self.main_window.data)
                #call the data_dumper function 
            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(self.update_rate)

    #function to dump the requests data out into json, then into dicts
    def data_dumper(self):
        dummy=0
        #self.main_window.data["CPU"] = all cpu info dumped out of the https response
        #after data is dumped and stored, call update pane_manager who will grab the new data and update the panes