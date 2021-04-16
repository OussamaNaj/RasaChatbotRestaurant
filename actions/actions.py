from rasa_sdk.forms import FormAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from database_connectivity import ComResAjout
from database_connectivity import modification
from database_connectivity import cancel,bill

# import transformers
# import torch
# tokenizer = transformers.AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
# model = transformers.AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
# text = r"""
# Tunisia,[a] officially the Republic of Tunisia,
#  is a country in the Maghreb region of North Africa. It is bordered by Algeria to the west and southwest,
#   Libya to the southeast, and the Mediterranean Sea to the north and east; covering 163,610 km2 (63,170 sq mi), Tunisia is the smallest country in North Africa. It contains the eastern end of the Atlas Mountains and the northern reaches of the Sahara desert, with much of its remaining territory arable land. Its 1,300 km (810 mi) of coastline include the African conjunction of the western and eastern parts of the Mediterranean Basin. Tunisia's northernmost point, Cape Angela, is also the northernmost point of Africa. Its population was 11.7 million in 2019,[13] and the capital and largest city is Tunis, located on the northeast coast, which lends the country its name.
# From early antiquity, Tunisia was inhabited by the indigenous Berbers.
# In 2011, the Tunisian Revolution, triggered by the lack of freedom and democracy under the 24-year rule of president Zine El Abidine Ben Ali, overthrew his regime and catalyzed the broader Arab Spring across the region. Free multiparty parliamentary elections were held shortly after; the country again voted for parliament on 26 October 2014,[20] and for president on 23 November 2014.[21] Tunisia remains a unitary semi-presidential representative democratic republic; it is the only country in North Africa classified as "Free" by Freedom House,[22] and considered the only fully democratic state in the Arab World in the Economist Intelligence Unit's Democracy Index.[23][24][25][c] Tunisia has a high human development index[16] and one of the highest GDP per capita in Africa.
# """
#
#
# def resp(questions, text):
#     for question in questions:
#         inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
#         input_ids = inputs["input_ids"].tolist()[0]
#         outputs = model(**inputs)
#         answer_start_scores = outputs.start_logits
#         answer_end_scores = outputs.end_logits
#
#         answer_start = torch.argmax(
#             answer_start_scores
#         )  # Get the most likely beginning of answer with the argmax of the score
#         answer_end = torch.argmax(
#             answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score
#
#         answer = tokenizer.convert_tokens_to_string(
#             tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     return answer

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

        dispatcher.utter_message(text="")
        cancel(tracker.get_slot("code"))

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

        dispatcher.utter_message(text="")
        modification(tracker.get_slot("modification"),tracker.get_slot("code"))

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

        res=bill(tracker.get_slot("code"))
        dispatcher.utter_message(text="Your Bill is : " + str(res)+"$")
        return []
