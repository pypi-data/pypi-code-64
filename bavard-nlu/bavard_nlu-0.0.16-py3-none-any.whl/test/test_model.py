import json
from unittest import TestCase

from bavard_nlu.model import NLUModel
from bavard_nlu.data_preprocessing.prediction_input import PredictionInput


class TestModel(TestCase):
    def setUp(self):
        super().setUp()
        self.max_seq_len = 200
        self.tokenizer = NLUModel.get_tokenizer()
        self.prediction_input = "how much is a flight from washington to boston"
        with open("test_data/test-agent.json") as f:
            self.agent_data = json.load(f)
    
    def test_train_and_predict(self):
        model = NLUModel(self.agent_data, self.max_seq_len)
        model.build_and_compile_model()
        model.train(batch_size=1, epochs=1)

        # Make the predictions.
        raw_intent_pred, raw_tags_pred = model.predict(
            self.prediction_input,
            self.tokenizer
        )

        # Decode the predictions.
        intent = model.decode_intent(raw_intent_pred)
        self.assertIn(intent, self.agent_data["nluData"]["intents"])

        pred_input = PredictionInput(self.prediction_input, self.max_seq_len, self.tokenizer)
        tags = model.decode_tags(raw_tags_pred, self.prediction_input, pred_input.word_start_mask)
        for tag in tags:
            self.assertIn(tag["tag_type"], self.agent_data["nluData"]["tagTypes"])
