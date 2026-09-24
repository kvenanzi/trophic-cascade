import warnings

import pytest
import torch

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture(scope="session")
def gpt2():
    from transformer_lens import HookedTransformer
    torch.set_grad_enabled(False)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    return HookedTransformer.from_pretrained("gpt2", device=dev)


@pytest.fixture(scope="session")
def prompts():
    from trophic.ioi import make_prompts, single_token_vocab
    return make_prompts(2, single_token_vocab(), seed=0)
