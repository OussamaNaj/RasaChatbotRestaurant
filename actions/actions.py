from rasa_sdk.forms import FormAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import ComResAjout
from database_connectivity import modification
from database_connectivity import cancel,bill,verif
from zina import takeCommand


class ActionHelloWorld1(FormAction):
    reservation=""
    command = ""
    def name(self) -> Text:
        return "reservation_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["reservation"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        ll=["Can i","we want","i have","give me","i want","i can","i would","i would like","I'd like","get","have","had","need","reserve","book","sit","choose","i wanna"]
        for j in ll:
            if (j.upper() in self.reservation.upper()):
                self.reservation=self.reservation.upper().replace(j.upper(),"")
        id = ComResAjout("nothing", self.reservation)
        dispatcher.utter_message(text="Done !")
        dispatcher.utter_message(text="your Code is: "+str(id))
        return []

class ActionHelloWorld2(FormAction):
    command=""
    reservation = ""
    def name(self) -> Text:
        return "command_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["command"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        l=["Can i","i have","give me","i want","i can","i would","i would like","I'd like","get","have","had","i wanna"]
        for i in l:
            if (i.upper() in self.command.upper()):
                self.command=self.command.upper().replace(i.upper(),"")
        id = ComResAjout(self.command,"nothing")
        dispatcher.utter_message(text="Done !")
        dispatcher.utter_message(text="Your Code is: "+ str(id))

        return []
class ActionHelloWorld3(FormAction):
    reservation=""
    command=""

    def name(self) -> Text:
        return "reservation_command_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["command","reservation"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        l=["i Can","we want","i have","give me","i want","can i","i can","i would","i would like","I'd like","get","i have","had","i wanna"]
        for i in l:
            if (i.upper() in self.command.upper()):
                self.command=self.command.upper().replace(i.upper(),"")
        ll=["i Can","can i","i have","give me","i want","can i","i would","i would like","I'd like","get","have","had","i need","reserve","book","sit","choose","i wanna"]
        for j in ll:
            if (j.upper() in self.reservation.upper()):
                self.reservation=self.reservation.upper().replace(j.upper(),"")
        id = ComResAjout(self.command,self.reservation)
        dispatcher.utter_message(text="Done !")
        dispatcher.utter_message(text="Your Code is :"+str(id))
        return []
class ActionHelloWorld4(FormAction):

    def name(self) -> Text:
        return "cancel_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["code"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        myresult=verif(tracker.get_slot("code"))
        if myresult == []:
            dispatcher.utter_message(text="The code is wrong, try again please !!")
        else:
            cancel(tracker.get_slot("code"))
        return []

class ActionHelloWorld5(FormAction):
    modification=""
    def name(self) -> Text:
        return "modification_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["modification","code"]

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        var=tracker.get_slot("modification")
        l=["i Can","i Can","we want to","i have to","i want to","can i","i would to","i would like to","I'd like to","i have to","had","i wanna to"]
        for i in l:
            if (i.upper() in self.modification.upper()):
                self.modification=self.modification.upper().replace(i.upper(),"")
        myresult=verif(tracker.get_slot("code"))
        if myresult == []:
            dispatcher.utter_message(text="The code is wrong, try again please !!")
        else:
            modification(self.modification,tracker.get_slot("code"))
        return []

class ActionHelloWorld6(FormAction):

    def name(self) -> Text:
        return "bill_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["code"]

    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        myresult=verif(tracker.get_slot("code"))
        if myresult == []:
            dispatcher.utter_message(text="The code is wrong, try again please !!")
        else:
            res = bill(tracker.get_slot("code"))
            dispatcher.utter_message(text="Your Bill is : " + str(res) + "$")


        return []

class ActionHelloWorld7(FormAction):

    def name(self) -> Text:
        return "web_scraping"

    # this is how i can take the user message :
    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        rep=takeCommand(message)
        dispatcher.utter_message(text=rep)
        return

class ActionHelloWorld10(FormAction):

    def name(self) -> Text:
        return "aux_command_reservation"
    def run(self, dispatcher, tracker, domain):
        ActionHelloWorld1.command=tracker.latest_message["text"]
        ActionHelloWorld2.command = tracker.latest_message["text"]
        ActionHelloWorld3.command = tracker.latest_message["text"]
        return

class ActionHelloWorld11(FormAction):

    def name(self) -> Text:
        return "aux_reservation_command"
    def run(self, dispatcher, tracker, domain):
        ActionHelloWorld3.reservation=tracker.latest_message["text"]
        ActionHelloWorld2.reservation = tracker.latest_message["text"]
        ActionHelloWorld1.reservation = tracker.latest_message["text"]
        return

class ActionHelloWorld12(FormAction):

    def name(self) -> Text:
        return "aux_modification"
    def run(self, dispatcher, tracker, domain):
        ActionHelloWorld5.modification=tracker.latest_message["text"]
        return
