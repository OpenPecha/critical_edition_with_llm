from pathlib import Path

from antx import transfer

from Pydurma.encoder import Encoder
from Pydurma.bo.tokenizer_bo import TibetanTokenizer, TibetanNormalizer
from Pydurma.aligners.fdmp import FDMPaligner
from Pydurma.input_filters.pattern_filter import PatternInputFilter
from Pydurma.weighers.matrix_weigher import TokenMatrixWeigher
from Pydurma.weighers.token_weigher_count import TokenCountWeigher
from Pydurma.serializers.hfml import HFMLSerializer
from Pydurma.serializers.plain_text import PlainTextSerializer
from Pydurma.commonspeller import CommonSpeller


def get_common_spell_text(version_paths, base_version_path):
    filter_patterns = []
    common_speller = CommonSpeller(FDMPaligner(), 
                                   filter_patterns, 
                                   TibetanTokenizer(Encoder(), 
                                    TibetanNormalizer(keep_eol=False)), 
                                    version_paths=version_paths,
                                    examplar_version_path=base_version_path)
    token_matrix = common_speller.get_common_spell_matrix()
    tokenMatrixWeigher = TokenMatrixWeigher()
    weighers = [TokenCountWeigher()]

    for weigher in weighers:
        tokenMatrixWeigher.add_weigher(weigher, weigher_weight=1)
    weighted_matrix = tokenMatrixWeigher.get_weight_matrix(token_matrix)
    version_paths = [base_version_path] + version_paths
    serializer = HFMLSerializer(weighted_token_matrix=weighted_matrix,
                                output_dir='./data/common_spell_text',
                                text_id='common_spell_text',
                                version_paths=version_paths,
                                verions_to_serialize={}
                                )
    serialized_text = serializer.serialize_matrix()
    return serialized_text



if __name__ == "__main__":
    version_paths = list(Path('./data/Chujuk').iterdir())
    version_paths.sort()
    base_version_path = Path('./data/Chujuk/02derge.txt')
    version_paths.remove(base_version_path)
    serialized_text = get_common_spell_text(version_paths, base_version_path)
    # serialized_text = serialized_text.replace('\n', '')
    # base_version = base_version_path.read_text(encoding='utf-8')
    # patterns = [['linebreak', '(\n)']]
    # serialized_text = transfer(base_version, patterns, serialized_text)
    Path('./data/common_spell_text.txt').write_text(serialized_text)


