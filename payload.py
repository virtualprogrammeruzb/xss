import json
import requests

class PayloadInformation( ):
    def __init__(self, key ,payload_name):

        self.key = key
        self.payload_name = payload_name
        
        for payload in payload_name.values():
            payload
           
        return


    def __str__(self):
        return f"{self.key} ({self.payload_name}) "

class PayloadsInfo():
    def __init__(self,payload_file_path=None):

        if payload_file_path is None:
            payload_file_path = "file qoshilgan joyga import qilinadi"##########################
            if not payload_file_path.lower().endswith(".json"):
                 raise  FileNotFoundError(f"Incorrect Json file extension for payloads")
            if "http://" == payload_file_path[:7].lower() or "https://" == payload_file_path[:8].lower():
                 
                try:
                    response = requests.get(url=payload_file_path)
                except:
                    raise FileNotFoundError(f"Problem While attempting to access"
                                            f"payload file URL  '{payload_file_path}':  "
                                            )
                if response.status_code == 200:
                    try:
                        payload_data = response.json()
                    except Exception as error:
                        raise ValueError(f"Problem parsing json content at"
                                         f" '{payload_file_path}': {str(error)}."
                                         )
                else:
                   raise FileNotFoundError(f"Bad response while accessing"
                                           f" data file URL '{payload_file_path}'"
                                           )

            else:
                try:
                    with open(payload_file_path, "r", encoding="utf-8") as file:
                         try:
                             payload_data = json.load(file)
                         except Exception as error:
                             raise ValueError (f"Problem parsing json contents at"
                                               f"'{payload_file_path}' : {str(error)}."

                                              )
                except FileNotFoundError as error:
                    raise FileNotFoundError (f"Problem while attempting to access"
                                             f"payload file '{payload_file_path}'."
                                            )


        f =open('payload.json', 'r',  encoding="utf-8")
        payload_data = json.load(f)
        
        self.payloads = {}
        for payload_name in payload_data:
            try:
                self.payloads[payload_name]  = \
                    PayloadInformation(payload_name,
                                       payload_data[payload_name]
                                      )
            except KeyError as error:
                raise ValueError(f"Problem parsing json contents at "
                                 f"'{payload_file_path}' : "
                                 f"Missing attribute {str(error)}."
                                )


        return

    def __iter__(self):


        for payload_name in self.payloads:
            yield self.payloads[payload_name]
             


    def __len__(self):

        return len(self.payloads)

if __name__ == '__main__':
    PayloadsInfo('payload.json')
