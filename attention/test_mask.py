import pytest
from transformers import AutoTokenizer, TFBertForMaskedLM
from mask import get_mask_token_index, get_color_for_attention_score, visualize_attentions

# Pre-trained masked language model
MODEL = "bert-base-uncased"


def test_get_mask_token_index():
    # Tokenizer input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    
    # Case #1
    text = "I am good."
    inputs = tokenizer(text, return_tensors="tf")
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)

    assert mask_token_index is None

    # Case #2
    text = "We turned down a narrow lane and passed through a small [MASK]"
    # text = "Then I picked up a [MASK] from the table."
    
    inputs = tokenizer(text, return_tensors="tf")
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    
    assert mask_token_index == 12


def test_get_color_for_attention_score():
    attention_score = 0
    color = get_color_for_attention_score(attention_score)
    assert color == (0, 0, 0)

    attention_score = 1
    color = get_color_for_attention_score(attention_score)
    assert color == (255, 255, 255)

    attention_score = 0.37
    color = get_color_for_attention_score(attention_score)
    assert color == (94, 94, 94)


if __name__ == "__main__":
    pytest.main()