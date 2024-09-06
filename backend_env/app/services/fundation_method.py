import random
import numpy

SLOT_FILL_THRESHOLD = 0.80
SUBJECT_FILL_THRESHOLD = 0.80

class Slot:
    """
    slot(dict): スロットの値
        "subjects"(dict): 誘発要因の大区分
            "subject_i"(dict): 誘発要因
                "triggers"(dict): トリガー
                    "trigger_i"(dict): トリガーに対応する値
                        "value"(dict): 誘発要因の程度・値
                        "status"(dict): 誘発要因の状態
                "status"(dict): 大区分の状態
        "status"(dict): スロットの状態
    """
    def __init__(self):
        self.slot = {}

    
    def get_subjects(self) -> list:
        return list(self.slot["subjects"].keys())


    def get_triggers(self) -> dict[str, list]:
        return {subject: list(self.slot["subjects"][subject]["triggers"].keys()) for subject in self.get_subjects()}
    

    def get_statistic(self) -> dict:
        """
        統計情報の取得
        Returns:
            result(dict): 統計情報
                fill_rate: スロットの埋まり具合
        """
        # 誘発要因ごとの埋まり具合を取得
        result = {"subjects": {}}
        for subject in self.get_subjects():
            fill_num = 0
            for trigger in self.get_triggers(subject):
                fill_num += 1 if self.slot["subjects"][subject]["triggers"][trigger]["status"]["fill_flag"] else 0
            trigger_num = len(list(self.slot["subjects"][subject]["triggers"].keys()))
            result["subjects"][subject] = {}
            result["subjects"][subject]["fill_num"] = fill_num
            result["subjects"][subject]["trigger_num"] = trigger_num
            result["subjects"][subject]["fill_rate"] = fill_num / trigger_num
        all_fill_num = numpy.sum([result["subjects"][subject]["fill_num"] for subject in self.get_subjects()])
        all_trigger_num = numpy.sum([result["subjects"][subject]["trigger_num"] for subject in self.get_subjects()])
        result["fill_rate"] = all_fill_num / all_trigger_num
        # ...

        return result

    @staticmethod
    def make_slot_from_QT(question_table:dict[str, any]) -> dict:
        """
        質問テーブルからスロットを生成
        Args:
            question_table(dict): 質問テーブル
        Returns:
            slot(dict): スロット
        """
        slot = {}
        for question in question_table:
            trigger = question.trigger
            subject = question.subject
            if subject not in slot:
                slot[subject] = {"triggers": {}}
            if trigger not in slot[subject]["triggers"]:
                slot[subject]["triggers"][trigger] = {"value": {}, "status": {"fill_flag": False}}
        return slot

    def __str__(self):
        return f"subject: {self.subject},\n slot: {self.slot}"
    

    def __repr__(self):
        return self.__str__()



class QuestionTable:
    def __init__(self, question_table:dict={}):
        self.question_table = self.set_question_table(question_table)


    def set_question_table(self, question_table:dict):
        self.question_table = question_table


    def __str__(self):
        return f"question_table: {self.question_table}"
    

    def __repr__(self):
        return self.__str__()
    

def generate_question(slot:Slot, question_table:dict[str, any]) -> str:
    """
    スロットを埋めるための最適な質問を生成する
    Args:
        slot (dict): スロット
        question_table: 質問テーブル
    Returns:
        question(str): 質問文
    """
    # 主題・誘発要因の取得
    subjects = slot.get_subjects()
    triggers = slot.get_triggers()
    # slotとquestion_tableの整合性を確認
    # TODO: ここで整合性を確認する
    # スロットの埋まり具合から埋めたい誘発要因を取得
    slot_statistic = slot.get_statistic()
    subject_fill_rate = sorted([(subject, slot_statistic["subjects"][subject]["fill_rate"]) for subject in subjects], key=lambda x: x[1])
    target_subject = subject_fill_rate[0][0]
    target_trigger = sorted([(trigger, question_table["subjects"][target_subject]["triggers"][trigger]["priority"]) for trigger in triggers[target_subject]], key=lambda x: x[1], reverse=True)[0][0]
    # スロットに対応する質問を取得
    question_candidates = question_table["subjects"][target_subject]["triggers"][target_trigger]["questions"]
    question = random.choice(question_candidates)
    return question




