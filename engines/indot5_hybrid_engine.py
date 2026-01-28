"""
IndoT5 Hybrid Paraphraser Engine
Combines IndoT5 neural processing with rule-based transformations
Following hybrid approach: Neural generation -> Rule-based enhancement
"""

import json
import os
import re
import random
import logging
import time
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
import nltk
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IndoT5HybridResult:
    """Result container for IndoT5 hybrid paraphrasing"""
    original_text: str
    paraphrased_text: str
    method_used: str
    transformations_applied: List[str]
    quality_score: float
    confidence_score: float
    neural_confidence: float
    semantic_similarity: float
    lexical_diversity: float
    syntactic_complexity: float
    fluency_score: float
    processing_time: float
    word_changes: int
    syntax_changes: int
    success: bool = True
    error_message: Optional[str] = None
    alternatives: List[str] = field(default_factory=list)

class IndoT5HybridParaphraser:
    """
    IndoT5 Hybrid Paraphraser Engine
    
    Combines IndoT5 neural processing with rule-based transformations:
    1. IndoT5 neural generation for initial paraphrase
    2. Rule-based enhancement (synonym substitution, syntactic transformation)
    3. Quality assessment and validation
    """
    
    def __init__(self, 
                 model_name: str = "Wikidepia/IndoT5-base",
                 use_gpu: bool = True,
                 synonym_rate: float = 0.7,
                 min_confidence: float = 0.5,
                 quality_threshold: float = 60.0,
                 max_transformations: int = 5,
                 enable_caching: bool = True):
        """
        Initialize IndoT5 Hybrid Paraphraser
        
        Args:
            model_name: IndoT5 model name
            use_gpu: Whether to use GPU acceleration
            synonym_rate: Synonym replacement rate (0.0-1.0)
            min_confidence: Minimum neural confidence threshold
            quality_threshold: Minimum quality score threshold
            max_transformations: Maximum rule-based transformations
            enable_caching: Enable model and result caching
        """
        self.model_name = model_name
        self.use_gpu = use_gpu and torch.cuda.is_available()
        self.synonym_rate = synonym_rate
        self.min_confidence = min_confidence
        self.quality_threshold = quality_threshold
        self.max_transformations = max_transformations
        self.enable_caching = enable_caching
        
        # Initialize device
        self.device = torch.device("cuda" if self.use_gpu else "cpu")
        
        # Initialize models
        self._init_models()
        
        # Load data
        self._load_data()
        
        # Initialize caches
        if self.enable_caching:
            self._result_cache = {}
            self._synonym_cache = {}
            self._similarity_cache = {}  # Cache for semantic similarity
        
        logger.info(f"✅ IndoT5 Hybrid Paraphraser initialized")
        logger.info(f"   Model: {self.model_name}")
        logger.info(f"   Device: {self.device}")
        logger.info(f"   GPU: {self.use_gpu}")
    
    def _init_models(self):
        """Initialize IndoT5 and semantic similarity models"""
        try:
            # Load IndoT5 model
            logger.info(f"🔄 Loading IndoT5 model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                use_fast=False,
                legacy=True
            )
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            
            if self.use_gpu:
                self.model = self.model.to(self.device)
            
            # Load semantic similarity model
            logger.info("🔄 Loading semantic similarity model")
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            logger.info("✅ Models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            raise
    
    def _load_data(self):
        """Load synonym database and transformation rules"""
        try:
            # Load synonym database
            current_dir = os.path.dirname(os.path.abspath(__file__))
            synonym_path = os.path.join(current_dir, "..", "data", "sinonim_extended.json")
            
            if os.path.exists(synonym_path):
                with open(synonym_path, 'r', encoding='utf-8') as f:
                    self.synonym_data = json.load(f)
                logger.info(f"✅ Loaded {len(self.synonym_data)} synonyms")
            else:
                logger.warning("⚠️  Synonym file not found, using empty dictionary")
                self.synonym_data = {}
            
            # Load transformation rules
            rules_path = os.path.join(current_dir, "..", "data", "transformation_rules.json")
            
            if os.path.exists(rules_path):
                with open(rules_path, 'r', encoding='utf-8') as f:
                    self.transformation_rules = json.load(f)
                logger.info("✅ Loaded transformation rules")
            else:
                logger.warning("⚠️  Transformation rules not found, using defaults")
                self.transformation_rules = self._get_default_rules()
            
            # Load stopwords
            stopwords_path = os.path.join(current_dir, "..", "data", "stopwords_id.txt")
            
            if os.path.exists(stopwords_path):
                with open(stopwords_path, 'r', encoding='utf-8') as f:
                    self.stop_words = set(line.strip() for line in f.readlines())
                logger.info(f"✅ Loaded {len(self.stop_words)} stopwords")
            else:
                logger.warning("⚠️  Stopwords file not found, using defaults")
                self.stop_words = self._get_default_stopwords()
            
        except Exception as e:
            logger.error(f"❌ Error loading data: {e}")
            # Use default data
            self.synonym_data = {}
            self.transformation_rules = self._get_default_rules()
            self.stop_words = self._get_default_stopwords()
    
    def _get_default_rules(self) -> Dict[str, List[Dict[str, str]]]:
        """Get default transformation rules"""
        return {
            "active_to_passive": [
                {"pattern": r"(\w+)\s+(me\w+)\s+(\w+)", "replacement": r"\3 di\2 oleh \1"},
                {"pattern": r"(\w+)\s+(akan|telah)\s+(\w+)\s+(\w+)", "replacement": r"\4 \2 di\3 oleh \1"}
            ],
            "conjunction_substitution": [
                {"pattern": r"\bdan\b", "replacement": "serta"},
                {"pattern": r"\btetapi\b", "replacement": "namun"},
                {"pattern": r"\bkarena\b", "replacement": "sebab"},
                {"pattern": r"\bjika\b", "replacement": "apabila"}
            ],
            "modifier_adjustment": [
                {"pattern": r"\bsangat\s+(\w+)", "replacement": r"amat \1"},
                {"pattern": r"\bcukup\s+(\w+)", "replacement": r"agak \1"}
            ]
        }
    
    def _get_default_stopwords(self) -> set:
        """Get default Indonesian stopwords"""
        return {
            'dan', 'atau', 'yang', 'adalah', 'dengan', 'untuk', 'dalam', 'dari', 
            'pada', 'ke', 'di', 'ini', 'itu', 'akan', 'dapat', 'juga', 'tidak',
            'ada', 'sudah', 'telah', 'harus', 'bisa', 'lebih', 'sangat', 'saya',
            'kami', 'kita', 'mereka', 'dia', 'ia', 'anda', 'kamu', 'maka',
            'oleh', 'bila', 'jika', 'ketika', 'saat', 'waktu', 'dimana', 'bagaimana',
            'mengapa', 'kenapa', 'siapa', 'apa', 'kapan', 'namun', 'tetapi',
            'karena', 'sebab', 'sehingga', 'meski', 'walaupun', 'meskipun'
        }
    
    def _neural_paraphrase(self, text: str, num_beams: int = 4, temperature: float = 1.2) -> Tuple[str, float]:
        """
        Generate paraphrase using IndoT5 neural model (IMPROVED QUALITY & DIVERSITY)
        
        Args:
            text: Input text
            num_beams: Number of beams for beam search
            temperature: Temperature for generation
            
        Returns:
            Tuple of (paraphrased_text, confidence_score)
        """
        try:
            # Try multiple strategies to get best result
            strategies = [
                ("parafrasekan", 1.3),      # Strategy 1: formal, higher temp
                ("tulis ulang", 1.1),       # Strategy 2: creative, normal temp
            ]
            
            all_candidates = []
            
            for prefix, temp in strategies:
                prefix_text = f"{prefix}: {text}"
                
                inputs = self.tokenizer(
                    prefix_text,
                    return_tensors="pt",
                    max_length=512,
                    truncation=True,
                    padding=True
                )
            
                if self.use_gpu:
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Add randomization for diversity
                actual_temp = temp + random.uniform(-0.15, 0.25)
                actual_temp = max(0.9, min(1.8, actual_temp))
                
                # Generate with both beam search and sampling
                with torch.no_grad():
                    # Beam search results
                    outputs = self.model.generate(
                        **inputs,
                        max_length=min(len(text.split()) * 2 + 50, 256),
                        min_length=max(len(text.split()) - 5, 5),
                        num_beams=num_beams,
                        num_return_sequences=2,  # Get 2 candidates per strategy
                        do_sample=True,
                        temperature=actual_temp,
                        top_k=60,
                        top_p=0.93,
                        early_stopping=True,
                        repetition_penalty=1.5,
                        length_penalty=0.8,
                        no_repeat_ngram_size=3,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                
                # Process all candidates
                for output in outputs:
                    import re
                    decoded = self.tokenizer.decode(output, skip_special_tokens=True).strip()
                    
                    # ROBUST prefix removal - only at start of text
                    prefixes_to_remove = [
                        r'^parafrasekan\s*:\s*',
                        r'^tulis\s+ulang\s*:\s*',
                        r'^tulis\s*:\s*',
                        r'^ulang\s*:\s*',
                        r'^dengan\s+kata\s+berbeda\s*:\s*',
                        r'^kata\s+berbeda\s*:\s*',
                        r'^kata\s+beda\s*:\s*',
                    ]
                    
                    for pattern in prefixes_to_remove:
                        decoded = re.sub(pattern, '', decoded, flags=re.IGNORECASE)
                    
                    # Remove any garbage like "an:fratuktur:" or "frafaksi:" at start
                    # Match pattern like: word:word: at the beginning
                    decoded = re.sub(r'^[a-z]+:[a-z]+:\s*', '', decoded, flags=re.IGNORECASE)
                    
                    # Clean up multiple punctuation
                    decoded = re.sub(r'\s+', ' ', decoded)
                    decoded = re.sub(r'\.{2,}', '.', decoded)
                    decoded = re.sub(r':{2,}', ':', decoded)
                    decoded = re.sub(r'-{2,}', '-', decoded)
                    decoded = decoded.strip(': .-,')
                    
                    # STRICT VALIDATION
                    if decoded and self._is_valid_paraphrase(text, decoded):
                        all_candidates.append(decoded)
            
            # Select best candidate
            if all_candidates:
                # Score each candidate
                best_candidate = None
                best_score = -1
                
                for candidate in all_candidates:
                    similarity = self._calculate_semantic_similarity(text, candidate)
                    word_overlap = len(set(text.lower().split()) & set(candidate.lower().split())) / len(set(text.lower().split()))
                    
                    # Score: high semantic (0.75) + diversity (0.25)
                    score = similarity * 0.75 + (1.0 - word_overlap) * 0.25
                    
                    if score > best_score:
                        best_score = score
                        best_candidate = candidate
                
                if best_candidate:
                    confidence = self._calculate_semantic_similarity(text, best_candidate)
                    return best_candidate, confidence
            
            # Fallback to rule-based
            logger.warning("⚠️ No valid neural candidates, using rule-based fallback")
            fallback_result, _, _ = self._apply_synonym_substitution(text, rate=0.6)
            if fallback_result != text:
                return fallback_result, 0.5
            else:
                return text, 0.3
            
        except Exception as e:
            logger.error(f"❌ Neural paraphrase failed: {e}")
            return text, 0.0
    
    def _is_valid_paraphrase(self, original: str, paraphrase: str) -> bool:
        """Validate if paraphrase is good quality"""
        import re
        
        # Basic checks
        if not paraphrase or len(paraphrase.split()) < 3 or paraphrase.lower() == original.lower():
            return False
        
        # Excessive char repetition
        if re.search(r'(.)\1{3,}', paraphrase):
            return False
        
        # Word repetition
        words = paraphrase.split()
        if len(words) > 0:
            max_word_freq = max([words.count(w) for w in set(words)])
            if max_word_freq / len(words) > 0.3:
                return False
            
            # Colon-heavy words
            colon_words = [w for w in words if ':' in w]
            if len(colon_words) > 2:
                return False
        
        # Too many special chars
        special_chars = sum(1 for c in paraphrase if not c.isalnum() and c not in ' .,!?;:-')
        if special_chars / max(len(paraphrase), 1) > 0.10:
            return False
        
        # Invalid patterns
        if 'kan:' in paraphrase or paraphrase.count('ulang') > 2:
            return False
        
        # Word length check
        words = [w for w in paraphrase.split() if len(w) > 2]
        if len(words) < 2:
            return False
        
        avg_word_len = sum(len(w) for w in words) / max(len(words), 1)
        if avg_word_len < 3 or avg_word_len > 15:
            return False
        
        return True
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity using sentence transformers (WITH CACHING)
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        try:
            # Check cache first
            cache_key = f"{text1[:100]}||{text2[:100]}"  # Use first 100 chars for key
            if self.enable_caching and hasattr(self, '_similarity_cache'):
                if cache_key in self._similarity_cache:
                    return self._similarity_cache[cache_key]
            
            # Encode both texts using semantic_model (not similarity_model!)
            embeddings = self.semantic_model.encode([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            # Cache result
            if self.enable_caching and hasattr(self, '_similarity_cache'):
                self._similarity_cache[cache_key] = float(similarity)
            
            return float(similarity)
        except Exception as e:
            logger.warning(f"Semantic similarity calculation failed: {e}")
            # Fallback to quick similarity
            return self._quick_similarity(text1, text2)
    
    def _quick_similarity(self, text1: str, text2: str) -> float:
        """Fast similarity calculation without heavy semantic model"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return 1.0 - (intersection / union) if union > 0 else 0.0
    
    def _apply_synonym_substitution(self, text: str, rate: float = None) -> Tuple[str, List[str], int]:
        """
        Apply synonym substitution to text
        
        Args:
            text: Input text
            rate: Synonym replacement rate
            
        Returns:
            Tuple of (modified_text, transformations, changes_count)
        """
        if rate is None:
            rate = self.synonym_rate
        
        words = text.split()
        result = []
        transformations = []
        changes_count = 0
        
        for word in words:
            clean_word = word.lower().strip('.,!?;:"')
            
            # Skip stopwords and short words
            if clean_word in self.stop_words or len(clean_word) <= 2:
                result.append(word)
                continue
            
            # Check if word has synonyms
            if clean_word in self.synonym_data and random.random() < rate:
                # Handle both list format and dict format
                syn_data = self.synonym_data[clean_word]
                if isinstance(syn_data, list):
                    synonyms = syn_data
                elif isinstance(syn_data, dict):
                    synonyms = syn_data.get('sinonim', [])
                else:
                    synonyms = []
                
                if synonyms:
                    # Choose random synonym
                    chosen_synonym = random.choice(synonyms)
                    
                    # PREVENT DUPLICATE: Check if chosen synonym matches previous or next word
                    prev_word = result[-1].lower().strip('.,!?;:"') if result else ""
                    synonym_clean = chosen_synonym.lower().strip('.,!?;:"')
                    
                    # Skip if synonym would create "kunci kunci" type duplication
                    if synonym_clean == prev_word:
                        result.append(word)
                        continue
                    
                    # Preserve original word format
                    if word.isupper():
                        formatted_synonym = chosen_synonym.upper()
                    elif word.istitle():
                        formatted_synonym = chosen_synonym.title()
                    else:
                        formatted_synonym = chosen_synonym
                    
                    # Preserve punctuation
                    if word[-1] in '.,!?;:"':
                        formatted_synonym += word[-1]
                    
                    result.append(formatted_synonym)
                    transformations.append(f"synonym: {word} -> {formatted_synonym}")
                    changes_count += 1
                else:
                    result.append(word)
            else:
                result.append(word)
        
        return ' '.join(result), transformations, changes_count
    
    def _apply_syntactic_transformation(self, text: str, max_transforms: int = None) -> Tuple[str, List[str], int]:
        """
        Apply syntactic transformations to text
        
        Args:
            text: Input text
            max_transforms: Maximum number of transformations
            
        Returns:
            Tuple of (modified_text, transformations, changes_count)
        """
        if max_transforms is None:
            max_transforms = self.max_transformations
        
        result = text
        transformations = []
        changes_count = 0
        
        # Available transformation types
        transform_types = [
            "active_to_passive",
            "conjunction_substitution", 
            "modifier_adjustment"
        ]
        
        # Apply random transformations
        num_transforms = min(max_transforms, len(transform_types))
        selected_transforms = random.sample(transform_types, num_transforms)
        
        for transform_type in selected_transforms:
            if transform_type in self.transformation_rules:
                rules_data = self.transformation_rules[transform_type]
                
                # Handle list format (active_to_passive, modifier_adjustment)
                if isinstance(rules_data, list):
                    for rule in rules_data:
                        pattern = rule.get("pattern", "")
                        replacement = rule.get("replacement", "")
                        
                        if pattern and re.search(pattern, result, re.IGNORECASE):
                            new_result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
                            
                            if new_result != result:
                                transformations.append(f"syntactic: {transform_type}")
                                changes_count += 1
                                result = new_result
                                break  # Only apply one rule per type
                
                # Handle dict format (conjunction_substitution)
                elif isinstance(rules_data, dict):
                    for word, word_data in rules_data.items():
                        alternatives = word_data.get("alternatives", []) if isinstance(word_data, dict) else []
                        if alternatives and re.search(rf'\b{word}\b', result, re.IGNORECASE):
                            chosen = random.choice(alternatives)
                            new_result = re.sub(rf'\b{word}\b', chosen, result, count=1, flags=re.IGNORECASE)
                            
                            if new_result != result:
                                transformations.append(f"syntactic: {transform_type} ({word} -> {chosen})")
                                changes_count += 1
                                result = new_result
                                break
        
        return result, transformations, changes_count
    
    def _apply_word_reordering(self, text: str) -> str:
        """
        Apply word reordering for better paraphrase variety
        Strategically reorder words while maintaining meaning
        """
        try:
            sentences = text.split('.')
            reordered_sentences = []
            
            for sentence in sentences:
                if not sentence.strip():
                    reordered_sentences.append(sentence)
                    continue
                
                words = sentence.strip().split()
                if len(words) <= 3:
                    reordered_sentences.append(sentence)
                    continue
                
                # Find adjectives and nouns to reorder
                # Simple heuristic: try to move adjectives or modifiers
                if random.random() < 0.4 and len(words) >= 4:
                    # Try swapping some words carefully
                    # Example: "yang sangat baik" -> "yang baik sangat" is ok
                    idx = random.randint(1, len(words) - 2)
                    if idx < len(words) - 1:
                        words[idx], words[idx + 1] = words[idx + 1], words[idx]
                
                reordered_sentences.append(' ' + ' '.join(words))
            
            result = '.'.join(reordered_sentences)
            return result.strip()
        except:
            return text
    
    def _calculate_quality_metrics(self, original: str, paraphrased: str, 
                                 neural_confidence: float, word_changes: int, 
                                 syntax_changes: int) -> Dict[str, float]:
        """
        Calculate comprehensive quality metrics
        
        Args:
            original: Original text
            paraphrased: Paraphrased text
            neural_confidence: Neural model confidence
            word_changes: Number of word changes
            syntax_changes: Number of syntax changes
            
        Returns:
            Dictionary of quality metrics
        """
        # Semantic similarity
        try:
            embeddings = self.semantic_model.encode([original, paraphrased])
            semantic_similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        except:
            semantic_similarity = 0.8  # Default fallback
        
        # Lexical diversity
        original_words = set(original.lower().split())
        paraphrased_words = set(paraphrased.lower().split())
        
        if len(original_words) > 0:
            lexical_diversity = len(paraphrased_words - original_words) / len(original_words)
        else:
            lexical_diversity = 0.0
        
        # Syntactic complexity (simplified)
        syntactic_complexity = min(1.0, syntax_changes / 3.0)
        
        # Fluency (based on length and structure similarity)
        length_ratio = len(paraphrased.split()) / max(len(original.split()), 1)
        fluency_score = 1.0 - abs(1.0 - length_ratio) * 0.5
        
        # Overall quality score - lebih prioritas diversity
        quality_score = (
            semantic_similarity * 0.30 +
            lexical_diversity * 0.35 +
            syntactic_complexity * 0.20 +
            fluency_score * 0.15
        ) * 100
        
        return {
            "semantic_similarity": semantic_similarity,
            "lexical_diversity": lexical_diversity,
            "syntactic_complexity": syntactic_complexity,
            "fluency_score": fluency_score,
            "quality_score": quality_score
        }
    
    def paraphrase(self, text: str, method: str = "hybrid") -> IndoT5HybridResult:
        """
        Main paraphrasing method using hybrid approach
        
        Args:
            text: Input text to paraphrase
            method: Paraphrasing method ("hybrid", "neural", "rule-based")
            
        Returns:
            IndoT5HybridResult object
        """
        start_time = time.time()
        
        # Input validation
        if not text or not text.strip():
            return IndoT5HybridResult(
                original_text=text,
                paraphrased_text=text,
                method_used=method,
                transformations_applied=["Error: Empty input"],
                quality_score=0.0,
                confidence_score=0.0,
                neural_confidence=0.0,
                semantic_similarity=0.0,
                lexical_diversity=0.0,
                syntactic_complexity=0.0,
                fluency_score=0.0,
                processing_time=0.0,
                word_changes=0,
                syntax_changes=0,
                success=False,
                error_message="Empty input text"
            )
        
        # Check cache (include method in cache key)
        cache_key = f"{method}:{text}"
        if self.enable_caching and cache_key in self._result_cache:
            cached_result = self._result_cache[cache_key]
            cached_result.processing_time = time.time() - start_time
            return cached_result
        
        try:
            transformations_applied = []
            
            if method == "hybrid":
                # ENHANCED HYBRID: Strategic balance of neural + rule-based
                # Goal: Combine neural semantic accuracy with rule-based transformation diversity
                
                # Step 1: Neural paraphrase with IndoT5
                neural_result, neural_confidence = self._neural_paraphrase(text)
                transformations_applied.append(f"neural_generation (confidence: {neural_confidence:.2f})")
                
                word_changes = 0
                syntax_changes = 0
                
                # Step 2: Strategic Rule-based enhancement based on confidence
                if neural_confidence >= self.min_confidence and neural_result != text:
                    # GOOD confidence - Apply BALANCED enhancements to preserve semantics
                    current_text = neural_result
                    
                    # Moderate synonym substitution to enhance diversity
                    synonym_result, synonym_transforms, wc = self._apply_synonym_substitution(
                        current_text, rate=min(0.65, self.synonym_rate * 0.9)  # Moderate rate - preserve semantics
                    )
                    word_changes += wc
                    transformations_applied.extend(synonym_transforms[:4])
                    
                    # Moderate syntactic transformation
                    final_text, syntax_transforms, sc = self._apply_syntactic_transformation(
                        synonym_result, max_transforms=2  # Limited transforms for good neural results
                    )
                    syntax_changes += sc
                    transformations_applied.extend(syntax_transforms[:2])
                    
                    # Occasional word reordering for natural variation
                    if random.random() < 0.4:
                        final_text = self._apply_word_reordering(final_text)
                        transformations_applied.append("word_reordering")
                        
                else:
                    # LOW confidence - Apply AGGRESSIVE rule-based transformations
                    transformations_applied.append("low_confidence_fallback")
                    
                    # Apply stronger synonym substitution as fallback
                    current_text, synonym_transforms, wc = self._apply_synonym_substitution(
                        text, rate=min(0.85, self.synonym_rate * 1.2)  # Lebih tinggi untuk fallback
                    )
                    word_changes += wc
                    transformations_applied.extend(synonym_transforms[:6])
                    
                    # Apply multiple syntactic transformations
                    final_text, syntax_transforms, sc = self._apply_syntactic_transformation(
                        current_text, max_transforms=4  # More transforms for fallback
                    )
                    syntax_changes += sc
                    transformations_applied.extend(syntax_transforms[:3])
                    
                    # Always apply word reordering for aggressive fallback
                    final_text = self._apply_word_reordering(final_text)
                    transformations_applied.append("word_reordering")
            
            elif method == "neural":
                # Pure neural paraphrase
                final_text, neural_confidence = self._neural_paraphrase(text)
                transformations_applied.append("neural_generation")
                word_changes = len(set(text.lower().split()) - set(final_text.lower().split()))
                syntax_changes = 1 if final_text != text else 0
                
            elif method == "rule-based":
                # Pure rule-based paraphrase - ENHANCED
                neural_confidence = 0.0
                transformations_applied = []
                
                # Apply synonym substitution dengan rate yang TINGGI
                current_text, synonym_transforms, word_changes = self._apply_synonym_substitution(
                    text, rate=min(0.85, self.synonym_rate * 1.3)  # Tinggi rate untuk lebih banyak perubahan
                )
                transformations_applied.extend(synonym_transforms[:8])
                
                # Apply syntactic transformation dengan aggressive
                final_text, syntax_transforms, syntax_changes = self._apply_syntactic_transformation(
                    current_text, max_transforms=4  # Lebih banyak transformations
                )
                transformations_applied.extend(syntax_transforms[:4])
                
                # Extra: Apply additional word order variations
                if random.random() < 0.6:
                    # Shuffle some words but keep meaning
                    final_text = self._apply_word_reordering(final_text)
                    transformations_applied.append("word_reordering")
            
            else:
                raise ValueError(f"Unknown method: {method}")
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(
                text, final_text, neural_confidence, word_changes, syntax_changes
            )
            
            # Create result
            result = IndoT5HybridResult(
                original_text=text,
                paraphrased_text=final_text,
                method_used=method,
                transformations_applied=transformations_applied,
                quality_score=quality_metrics["quality_score"],
                confidence_score=min(neural_confidence + quality_metrics["quality_score"] / 100, 1.0),
                neural_confidence=neural_confidence,
                semantic_similarity=quality_metrics["semantic_similarity"],
                lexical_diversity=quality_metrics["lexical_diversity"], 
                syntactic_complexity=quality_metrics["syntactic_complexity"],
                fluency_score=quality_metrics["fluency_score"],
                processing_time=time.time() - start_time,
                word_changes=word_changes,
                syntax_changes=syntax_changes,
                success=True
            )
            
            # Cache result (include method in cache key)
            if self.enable_caching:
                self._result_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Paraphrase failed: {e}")
            return IndoT5HybridResult(
                original_text=text,
                paraphrased_text=text,
                method_used=method,
                transformations_applied=["Error: Processing failed"],
                quality_score=0.0,
                confidence_score=0.0,
                neural_confidence=0.0,
                semantic_similarity=0.0,
                lexical_diversity=0.0,
                syntactic_complexity=0.0,
                fluency_score=0.0,
                processing_time=time.time() - start_time,
                word_changes=0,
                syntax_changes=0,
                success=False,
                error_message=str(e)
            )
    
    def clear_cache(self, text: str = None):
        """Clear result cache for a specific text or all cache"""
        if self.enable_caching:
            if text:
                self._result_cache.pop(text, None)
            else:
                self._result_cache.clear()
    
    def generate_variations(self, text: str, num_variations: int = 5, method: str = "hybrid", min_quality_threshold: float = 70.0) -> List[IndoT5HybridResult]:
        """
        Generate multiple paraphrase variations (OPTIMIZED)
        
        Args:
            text: Input text
            num_variations: Number of variations to generate (default: 5)
            method: Paraphrasing method ("hybrid", "neural", "rule-based")
            min_quality_threshold: Minimum quality score (0-100) for filtering results (default: 70.0)
            
        Returns:
            List of IndoT5HybridResult objects sorted by quality score
        """
        logger.info(f"🔄 Generating {num_variations} variations...")
        start_time = time.time()
        
        variations = []
        seen_texts = set()
        
        # Clear cache for this text to ensure unique variations
        self.clear_cache(text)
        
        # Store original parameters
        original_rate = self.synonym_rate
        original_transforms = self.max_transformations
        original_caching = self.enable_caching
        
        # Disable caching for variations
        self.enable_caching = False
        
        try:
            for i in range(num_variations):
                logger.info(f"  📝 Variation {i+1}/{num_variations}...")
                
                # Adjust parameters for variation
                self.synonym_rate = min(1.0, original_rate + (i * 0.15))
                self.max_transformations = min(5, original_transforms + i)
                
                # Generate variation
                result = self.paraphrase(text, method=method)
                
                # Only add if unique
                if result.paraphrased_text not in seen_texts:
                    variations.append(result)
                    seen_texts.add(result.paraphrased_text)
                    logger.info(f"  ✅ Variation {i+1} completed (quality: {result.quality_score:.2f})")
                else:
                    logger.info(f"  ⚠️  Variation {i+1} duplicate, skipped")
        finally:
            # Restore original parameters
            self.synonym_rate = original_rate
            self.max_transformations = original_transforms
            self.enable_caching = original_caching
        
        # Sort by quality score
        variations.sort(key=lambda x: x.quality_score, reverse=True)
        
        # Filter by minimum quality threshold if specified
        if min_quality_threshold > 0:
            filtered = [v for v in variations if v.quality_score >= min_quality_threshold]
            # If filtering removes all results, return best available
            if filtered:
                return filtered
            else:
                logger.warning(f"No variations met quality threshold {min_quality_threshold}%. Returning best available.")
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Generated {len(variations)} unique variations in {elapsed:.2f}s")
        
        return variations
    
    def batch_paraphrase(self, texts: List[str], method: str = "hybrid") -> List[IndoT5HybridResult]:
        """
        Process multiple texts in batch
        
        Args:
            texts: List of input texts
            method: Paraphrasing method
            
        Returns:
            List of IndoT5HybridResult objects
        """
        results = []
        
        for i, text in enumerate(texts):
            logger.info(f"Processing {i+1}/{len(texts)}: {text[:50]}...")
            result = self.paraphrase(text, method=method)
            results.append(result)
        
        return results
    
    def paraphrase_with_analysis(self, text: str) -> IndoT5HybridResult:
        """
        Paraphrase with detailed analysis
        
        Args:
            text: Input text
            
        Returns:
            IndoT5HybridResult with detailed metrics
        """
        return self.paraphrase(text, method="hybrid")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model_name": self.model_name,
            "device": str(self.device),
            "use_gpu": self.use_gpu,
            "synonym_rate": self.synonym_rate,
            "min_confidence": self.min_confidence,
            "quality_threshold": self.quality_threshold,
            "max_transformations": self.max_transformations,
            "synonyms_loaded": len(self.synonym_data),
            "stopwords_loaded": len(self.stop_words)
        }

def create_indot5_hybrid_paraphraser(model_name: str = "Wikidepia/IndoT5-base", 
                                   **kwargs) -> IndoT5HybridParaphraser:
    """
    Factory function to create IndoT5 Hybrid Paraphraser
    
    Args:
        model_name: IndoT5 model name
        **kwargs: Additional parameters
        
    Returns:
        IndoT5HybridParaphraser instance
    """
    return IndoT5HybridParaphraser(model_name=model_name, **kwargs) 
