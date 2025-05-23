from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

def get_bleu_score(reference: str, hypothesis: str) -> float:
    """Calculate BLEU score using NLTK."""
    reference_tokens = reference.lower().split()
    hypothesis_tokens = hypothesis.lower().split()
    smoothie = SmoothingFunction().method4
    score = sentence_bleu([reference_tokens], hypothesis_tokens, smoothing_function=smoothie)
    return round(score, 4)

def get_rouge_score(reference: str, hypothesis: str) -> float:
    """Calculate ROUGE-L F1 score."""
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(reference, hypothesis)['rougeL'].fmeasure
    return round(score, 4)

def evaluate_answer(question: str, answer: str) -> float:
    """Combine BLEU and ROUGE for a final evaluation score."""
    bleu = get_bleu_score(question, answer)
    rouge = get_rouge_score(question, answer)
    combined_score = round((bleu + rouge) / 2, 4)
    return combined_score
