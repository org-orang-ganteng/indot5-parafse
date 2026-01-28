#!/usr/bin/env python3
"""
Quick test untuk parafrase - test 1 kalimat dengan cepat
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def quick_test():
    """Quick test dengan 1 kalimat"""
    
    print("🚀 Quick Paraphrase Test")
    print("=" * 70)
    
    # Initialize
    print("\n📦 Loading model (tunggu 5-10 detik)...")
    paraphraser = IndoT5HybridParaphraser(
        model_name="Wikidepia/IndoT5-base",
        use_gpu=False
    )
    print("✅ Model loaded!\n")
    
    # Test text
    text = "Teknologi kecerdasan buatan telah mengubah cara kita bekerja dan berkomunikasi."
    
    print(f"Original Text:")
    print(f"  {text}\n")
    print("-" * 70)
    
    # Test hybrid method
    print("\n🔄 Generating paraphrase (HYBRID method)...\n")
    result = paraphraser.paraphrase(text, method="hybrid")
    
    print(f"✨ Paraphrase Result:")
    print(f"  {result.paraphrased_text}\n")
    
    print(f"📊 Quality Metrics:")
    print(f"  • Quality Score: {result.quality_score:.2f}/100")
    print(f"  • Confidence: {result.confidence_score:.2f}")
    print(f"  • Semantic Similarity: {result.semantic_similarity:.2f}")
    print(f"  • Lexical Diversity: {result.lexical_diversity:.2f}")
    print(f"  • Processing Time: {result.processing_time:.2f}s")
    
    if result.transformations_applied:
        print(f"\n🔧 Transformations Applied:")
        for i, trans in enumerate(result.transformations_applied[:5], 1):
            print(f"  {i}. {trans}")
    
    print("\n" + "=" * 70)
    print("✅ Test completed!")
    
    # Test variations
    print("\n\n🎨 Generating 3 variations...\n")
    variations = paraphraser.generate_variations(text, num_variations=3, method="hybrid")
    
    for i, var in enumerate(variations, 1):
        print(f"Variation #{i} (Quality: {var.quality_score:.1f}):")
        print(f"  {var.paraphrased_text}\n")
    
    print("=" * 70)
    print("🎉 All tests completed successfully!")

if __name__ == "__main__":
    quick_test()
