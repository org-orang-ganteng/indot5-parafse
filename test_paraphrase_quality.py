#!/usr/bin/env python3
"""
Script untuk menguji kualitas parafrase IndoT5 Hybrid
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def test_paraphrase():
    """Test paraphrase dengan berbagai contoh kalimat"""
    
    print("🚀 Memulai testing paraphrase...")
    print("=" * 70)
    
    # Initialize paraphraser
    print("\n📦 Loading model...")
    paraphraser = IndoT5HybridParaphraser(
        model_name="Wikidepia/IndoT5-base",
        use_gpu=False,
        synonym_rate=0.3,
        min_confidence=0.6
    )
    
    # Test cases
    test_texts = [
        "Teknologi kecerdasan buatan telah mengubah cara kita bekerja dan berkomunikasi.",
        "Pendidikan adalah kunci untuk membuka pintu kesuksesan di masa depan.",
        "Indonesia memiliki keanekaragaman budaya yang sangat kaya dan beragam.",
        "Pemanasan global menjadi ancaman serius bagi kehidupan di bumi.",
        "Penelitian ini bertujuan untuk mengembangkan sistem parafrase bahasa Indonesia."
    ]
    
    print("\n✅ Model loaded successfully!\n")
    print("=" * 70)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📝 Test Case #{i}")
        print(f"Original: {text}")
        print("-" * 70)
        
        # Test different methods
        methods = ["neural", "rule-based", "hybrid"]
        
        for method in methods:
            print(f"\n🔄 Method: {method.upper()}")
            result = paraphraser.paraphrase(text, method=method)
            
            print(f"Paraphrase: {result.paraphrased_text}")
            print(f"Quality Score: {result.quality_score:.2f}")
            print(f"Confidence: {result.confidence_score:.2f}")
            print(f"Semantic Similarity: {result.semantic_similarity:.2f}")
            print(f"Processing Time: {result.processing_time:.2f}s")
            
            if result.transformations_applied:
                print(f"Transformations: {', '.join(result.transformations_applied[:3])}")
        
        print("=" * 70)
    
    # Test variations
    print("\n\n🎨 Testing Variations Generation")
    print("=" * 70)
    
    sample_text = "Penelitian ini bertujuan untuk mengembangkan sistem parafrase bahasa Indonesia."
    print(f"\nOriginal: {sample_text}")
    print("-" * 70)
    
    variations = paraphraser.generate_variations(sample_text, num_variations=3, method="hybrid")
    
    for i, var in enumerate(variations, 1):
        print(f"\n📌 Variation #{i}")
        print(f"Text: {var.paraphrased_text}")
        print(f"Quality: {var.quality_score:.2f}")
        print(f"Confidence: {var.confidence_score:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_paraphrase()
