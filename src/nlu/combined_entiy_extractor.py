import logging
import os
from rasa_nlu.extractors.crf_entity_extractor import CRFEntityExtractor

logger = logging.getLogger(__name__)


class CombinedExtractor(CRFEntityExtractor):
    name = "ner_combi"

    provides = ["entities"]

    requires = ["spacy_doc", "tokens"]

    def __is_name(self, token):
        if 'PER' in token.ent_type_:
            return True

        if 'PROPN' in token.pos_ and 'NE' in token.tag_ and 'MISC' in token.ent_type_:
            return True

        return False

    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        extracted = self.add_extractor_name(self.extract_entities(message))

        spacy_nlp = kwargs.get("spacy_nlp", None)
        _doc = spacy_nlp(message.text)
        _ents = [t.ent_iob_ + '-name' if self.__is_name(t) else 'O' for t in _doc]

        if 'B-name' in _ents or 'I-name' in _ents:
            try:
                _ents.index('B-name')
            except ValueError:
                logger.info('no B-name, replace firt I-name with B-name manually!')
                _ents[_ents.index('I-name')] = 'B-name'

        logger.info(_ents)
        message.set('spacy_doc', _doc)
        extracted_name = self.add_extractor_name(self._from_crf_to_json(message, _ents))
        extracted = extracted + extracted_name
        logger.info(extracted)
        message.set("entities", message.get("entities", []) + extracted,
                    add_to_output=True)

    @classmethod
    def load(cls,
             model_dir,  # type: Text
             model_metadata,  # type: Metadata
             cached_component,  # type: Optional[CombinedExtractor]
             **kwargs  # type: **Any
             ):
        # type: (...) -> CombinedExtractor
        from sklearn.externals import joblib

        if model_dir and model_metadata.get("entity_extractor_crf"):
            meta = model_metadata.get("entity_extractor_crf")
            ent_tagger = joblib.load(os.path.join(model_dir, meta["model_file"]))
            return CombinedExtractor(ent_tagger=ent_tagger,
                                     entity_crf_features=meta['crf_features'],
                                     entity_crf_BILOU_flag=meta['BILOU_flag'])
        else:
            return CombinedExtractor()

    def persist(self, model_dir):
        # type: (Text) -> Dict[Text, Any]
        """Persist this model into the passed directory.

        Returns the metadata necessary to load the model again."""

        from sklearn.externals import joblib

        if self.ent_tagger:
            model_file_name = os.path.join(model_dir, "crf_model.pkl")

            joblib.dump(self.ent_tagger, model_file_name)
            return {"entity_extractor_crf": {"model_file": "crf_model.pkl",
                                             "crf_features": self.crf_features,
                                             "BILOU_flag": self.BILOU_flag,
                                             "version": 1}}
        else:
            return {"entity_extractor_crf": None}
