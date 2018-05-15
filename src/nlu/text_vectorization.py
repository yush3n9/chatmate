import importlib
import io
import logging
import os
from typing import Any, Optional
from typing import Dict
from typing import Text

from future.utils import PY3
from rasa_nlu.components import Component
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.featurizers import Featurizer
from rasa_nlu.model import Metadata
from rasa_nlu.training_data import Message
from rasa_nlu.training_data import TrainingData

logger = logging.getLogger(__name__)


class TextVectorizer(Featurizer):
    name = "vectorizer"

    provides = ["text_features"]

    requires = ["spacy_doc"]

    def __init__(self, vectorizer_name="sklearn.feature_extraction.text.TfidfVectorizer"):
        #CountTextVectorizer
        pkg_class = vectorizer_name.rsplit('.', 1)
        module = importlib.import_module(pkg_class[0])
        my_class = getattr(module, pkg_class[1])
        self.vectorizer = my_class()

    @classmethod
    def create(cls, config):
        # type: (RasaNLUConfig) -> Component
        vectorizer_name = config.get("vectorizer")
        if vectorizer_name:
            return cls(vectorizer_name)
        else:
            return cls()

    def train(self, training_data, config, **kwargs):
        # type: (TrainingData, RasaNLUConfig, **Any) -> None
        self.vectorizer.fit([e.get("spacy_doc").text for e in training_data.training_examples])
        for example in training_data.training_examples:
            vec = self.vectorizer.transform([example.get("spacy_doc").text])
            example.set("text_features", vec)

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        import cloudpickle
        pkl_name = self.name + '.pkl'
        classifier_file = os.path.join(model_dir, pkl_name)
        with io.open(classifier_file, 'wb') as f:
            cloudpickle.dump(self, f)

        return {
            "vectorizer": pkl_name
        }

    @classmethod
    def load(cls, model_dir=None, model_metadata=None, cached_component=None, **kwargs):
        # type: (Text, Metadata, Optional[Component], **Any) -> TextVectorizer
        import cloudpickle

        if model_dir and model_metadata.get(TextVectorizer.name):
            _file = os.path.join(model_dir, model_metadata.get(TextVectorizer.name))
            with io.open(_file, 'rb') as f:  # pragma: no test
                if PY3:
                    return cloudpickle.load(f, encoding="latin-1")
                else:
                    return cloudpickle.load(f)
        else:
            return cls()

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        vec = self.vectorizer.transform([message.get("spacy_doc").text])
        message.set("text_features", vec)
