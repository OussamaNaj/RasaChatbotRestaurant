from rasa_sdk.forms import FormAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import ComResAjout
from database_connectivity import modification
from database_connectivity import cancel,bill,verif


class ActionHelloWorld1(FormAction):

    def name(self) -> Text:
        return "reservation_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["reservation"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        id = ComResAjout("nothing", tracker.get_slot("reservation"))
        dispatcher.utter_message(text="Done !")
        dispatcher.utter_message(text="your Code is: "+str(id))
        return []

class ActionHelloWorld2(FormAction):

    def name(self) -> Text:
        return "command_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["command"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        id = ComResAjout(tracker.get_slot("command"), "nothing")
        dispatcher.utter_message(text="Done !")
        dispatcher.utter_message(text="Your Code is: "+ str(id))

        return []
class ActionHelloWorld3(FormAction):

    def name(self) -> Text:
        return "reservation_command_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["command","reservation"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        id = ComResAjout(tracker.get_slot("command"), tracker.get_slot("reservation"))
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
            dispatcher.utter_message(text="Done !")
        return []

class ActionHelloWorld5(FormAction):

    def name(self) -> Text:
        return "modification_form"
    @staticmethod
    def required_slots(tracker:Tracker)->List[Text]:
        print("required_slots(tracker:Tracker)")
        return ["modification","code"]
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:
        myresult=verif(tracker.get_slot("code"))
        if myresult == []:
            dispatcher.utter_message(text="The code is wrong, try again please !!")
        else:
            modification(tracker.get_slot("modification"),tracker.get_slot("code"))
            dispatcher.utter_message(text="Done !")
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
