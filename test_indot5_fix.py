#!/usr/bin/env python3
"""
Test script untuk memverifikasi perbaikan IndoT5
"""

import sys
sys.path.insert(0, '/workspaces/indot5-parafse')

from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def test_indot5():
    print("="*60)
    print("🧪 Testing IndoT5 Neural Paraphrase Fix")
    print("="*60)
    
    # Initialize paraphraser
    print("\n📦 Initializing IndoT5 Hybrid Paraphraser...")
    paraphraser = IndoT5HybridParaphraser(
        model_name="Wikidepia/IndoT5-base",
        use_gpu=False,
        enable_caching=True
    )
    print("✅ Paraphraser initialized\n")
    
    # Test input
    text = "Teknologi artificial intelligence berkembang sangat pesat di era digital ini."
    
    print(f"📝 Input Text:")
    print(f"   {text}\n")
    
    # Test neural method
    print("🔬 Testing NEURAL method...")
    print("-"*60)
    
    results = paraphraser.generate_variations(text, num_variations=2, method="neural")
    
    print(f"\n✅ Generated {len(results)} variations:\n")
    
    for i, result in enumerate(results, 1):
        print(f"Variasi {i}:")
        print(f"  Text: {result.paraphrased_text}")
        print(f"  Quality Score: {result.quality_score:.2f}")
        print(f"  Semantic Similarity: {result.semantic_similarity:.2f}")
        print(f"  Method: {result.method_used}")
        print(f"  Success: {'✅' if result.success else '❌'}")
        print()
    
    # Test hybrid method
    print("\n🔬 Testing HYBRID method...")
    print("-"*60)
    
    results = paraphraser.generate_variations(text, num_variations=2, method="hybrid")
    
    print(f"\n✅ Generated {len(results)} variations:\n")
    
    for i, result in enumerate(results, 1):
        print(f"Variasi {i}:")
        print(f"  Text: {result.paraphrased_text}")
        print(f"  Quality Score: {result.quality_score:.2f}")
        print(f"  Semantic Similarity: {result.semantic_similarity:.2f}")
        print(f"  Method: {result.method_used}")
        print(f"  Success: {'✅' if result.success else '❌'}")
        print()
    
    print("="*60)
    print("✅ Test selesai!")
    print("="*60)

if __name__ == "__main__":
    test_indot5()
