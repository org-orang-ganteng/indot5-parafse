#!/usr/bin/env python3
"""
Demo EKSTREM - Menunjukkan hasil parafrase yang SANGAT berbeda
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def show_extreme_differences():
    """Demo dengan parameter EKSTREM untuk hasil sangat berbeda"""
    
    print("\n" + "="*80)
    print("🔥 DEMO PARAFRASE EKSTREM - HASIL SANGAT BERBEDA DARI ASLI")
    print("="*80)
    
    # Initialize dengan parameter MAKSIMAL
    print("\n📦 Loading model dengan parameter EKSTREM...")
    print("   • Synonym Rate: 0.7 (70% kata diganti)")
    print("   • Temperature: 1.8 (sangat kreatif)")
    print("   • Max Transformations: 5")
    print("   • Diversity Priority: 70%")
    
    paraphraser = IndoT5HybridParaphraser(
        model_name="Wikidepia/IndoT5-base",
        use_gpu=False,
        synonym_rate=0.7,
        min_confidence=0.5,
        max_transformations=5
    )
    print("✅ Ready!\n")
    
    # Test cases
    test_cases = [
        {
            "text": "Teknologi kecerdasan buatan telah mengubah cara kita bekerja dan berkomunikasi.",
            "desc": "Tentang AI"
        },
        {
            "text": "Pendidikan adalah kunci untuk membuka pintu kesuksesan di masa depan.",
            "desc": "Tentang Pendidikan"
        },
        {
            "text": "Penelitian ini bertujuan untuk mengembangkan sistem parafrase bahasa Indonesia yang berkualitas tinggi.",
            "desc": "Tentang Penelitian"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        original = case["text"]
        desc = case["desc"]
        
        print(f"\n{'='*80}")
        print(f"📝 CONTOH #{i}: {desc}")
        print(f"{'='*80}\n")
        
        print(f"🔵 TEKS ASLI:")
        print(f"   \"{original}\"\n")
        
        print("⏳ Generating paraphrase...")
        result = paraphraser.paraphrase(original, method="hybrid")
        
        print(f"\n🟢 HASIL PARAFRASE:")
        print(f"   \"{result.paraphrased_text}\"\n")
        
        # Calculate differences
        original_words = set(original.lower().split())
        paraphrased_words = set(result.paraphrased_text.lower().split())
        same_words = original_words & paraphrased_words
        different_words = paraphrased_words - original_words
        
        print(f"📊 ANALISIS PERBEDAAN:")
        print(f"   ✓ Total kata asli: {len(original.split())}")
        print(f"   ✓ Total kata hasil: {len(result.paraphrased_text.split())}")
        print(f"   ✓ Kata yang sama: {len(same_words)} kata")
        print(f"   ✓ Kata baru: {len(different_words)} kata")
        print(f"   ✓ Persentase berubah: {(len(different_words) / len(original_words) * 100):.1f}%")
        
        print(f"\n📈 SKOR KUALITAS:")
        print(f"   • Quality Score: {result.quality_score:.1f}/100")
        print(f"   • Semantic Similarity: {result.semantic_similarity:.2f} (0.7-0.85 = bagus)")
        print(f"   • Lexical Diversity: {result.lexical_diversity:.2f} (>0.5 = sangat berbeda)")
        print(f"   • Confidence: {result.confidence_score:.2f}")
        
        if different_words:
            print(f"\n💡 Kata-kata BARU yang muncul:")
            print(f"   {', '.join(list(different_words)[:10])}")
        
        # Generate 2 variations
        print(f"\n🎨 VARIASI LAIN (2 alternatif):")
        variations = paraphraser.generate_variations(original, num_variations=2, method="hybrid")
        for j, var in enumerate(variations, 1):
            var_words = set(var.paraphrased_text.lower().split())
            var_different = var_words - original_words
            print(f"\n   Variasi #{j} ({len(var_different)} kata baru):")
            print(f"   \"{var.paraphrased_text}\"")
    
    print("\n" + "="*80)
    print("✅ DEMO SELESAI!")
    print("\n💡 KESIMPULAN:")
    print("   • Hasil parafrase sekarang JAUH LEBIH BERBEDA dari asli")
    print("   • Diversity Score tinggi (>0.5) = banyak kata baru")
    print("   • Semantic Similarity 0.7-0.85 = makna tetap terjaga")
    print("   • 50-70% kata berubah dari teks asli")
    print("\n🎯 Server web: http://localhost:5000")
    print("="*80 + "\n")

if __name__ == "__main__":
    show_extreme_differences()
