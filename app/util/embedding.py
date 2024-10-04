from FlagEmbedding import BGEM3FlagModel


class BGEM3Embedding:
    _model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)

    def __init__(self, text: list[str]):
        self._embeddings = self.get_embeddings(text)

    def get_embeddings(self, text: list[str]):
        """
        참고 : https://huggingface.co/BAAI/bge-m3
        """

        # TODO: 고도화시 속성값 받아올 수 있도록 변경
        return self._model.encode(
            text,
            batch_size=12,
            max_length=8192,
            return_dense=True,
            return_sparse=True,
            return_colbert_vecs=False,
        )

    @property
    def dense_vector(self):
        return self._embeddings["dense_vecs"]

    @property
    def sparse_vector(self):
        return self._embeddings["lexical_weights"]
