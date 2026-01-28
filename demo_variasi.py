#!/usr/bin/env python3
"""
Demo untuk menunjukkan peningkatan variasi parafrase
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def compare_paraphrase():
    """Demo perbandingan hasil parafrase"""
    
    print("🎨 Demo Parafrase dengan Variasi Tinggi")
    print("=" * 80)
    
    # Initialize
    print("\n📦 Loading model (tunggu 5-10 detik)...")
    paraphraser = IndoT5HybridParaphraser(
        model_name="Wikidepia/IndoT5-base",
        use_gpu=False,
        synonym_rate=0.5,  # Tinggi untuk lebih banyak variasi
        min_confidence=0.6
    )
    print("✅ Model loaded!\n")
    
    # Test cases
    test_cases = [
        "Teknologi kecerdasan buatan telah mengubah cara kita bekerja dan berkomunikasi.",
        "Pendidikan adalah kunci untuk membuka pintu kesuksesan di masa depan.",
        "Indonesia memiliki keanekaragaman budaya yang sangat kaya dan beragam.",
    ]
    
    for i, original in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"📝 Contoh #{i}")
        print(f"{'='*80}")
        print(f"\n🔵 TEKS ASLI:")
        print(f"   {original}\n")
        
        # Generate paraphrase
        print("🔄 Generating paraphrases...\n")
        
        # Method 1: Neural
        result_neural = paraphraser.paraphrase(original, method="neural")
        print(f"✨ HASIL NEURAL:")
        print(f"   {result_neural.paraphrased_text}")
        print(f"   📊 Quality: {result_neural.quality_score:.1f} | Confidence: {result_neural.confidence_score:.2f}")
        print(f"   🎯 Similarity: {result_neural.semantic_similarity:.2f} | Diversity: {result_neural.lexical_diversity:.2f}\n")
        
        # Method 2: Hybrid
        result_hybrid = paraphraser.paraphrase(original, method="hybrid")
        print(f"✨ HASIL HYBRID:")
        print(f"   {result_hybrid.paraphrased_text}")
        print(f"   📊 Quality: {result_hybrid.quality_score:.1f} | Confidence: {result_hybrid.confidence_score:.2f}")
        print(f"   🎯 Similarity: {result_hybrid.semantic_similarity:.2f} | Diversity: {result_hybrid.lexical_diversity:.2f}\n")
        
        # Generate 3 variations
        print("🎨 VARIASI TAMBAHAN (Hybrid):")
        variations = paraphraser.generate_variations(original, num_variations=3, method="hybrid")
        for j, var in enumerate(variations, 1):
            print(f"\n   Variasi #{j}:")
            print(f"   {var.paraphrased_text}")
            print(f"   Quality: {var.quality_score:.1f} | Diversity: {var.lexical_diversity:.2f}")
        
        print()
    
    print("="*80)
    print("\n✅ Demo selesai!")
    print("\n💡 Tips:")
    print("   • Semakin tinggi Diversity Score (0.4-0.7), semakin berbeda dengan aslinya")
    print("   • Similarity Score 0.7-0.85 = makna tetap terjaga tapi kata-kata berbeda")
    print("   • Quality Score > 60 = hasil berkualitas baik")
    print("   • Method 'hybrid' menggabungkan kekuatan neural + rule-based")

if __name__ == "__main__":
    compare_paraphrase()
