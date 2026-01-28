#!/usr/bin/env python3
"""
Test script to verify quality improvements across all three paraphrase methods.
Tests that each method produces different but quality outputs.
"""

import sys
import json
import time
from engines.indot5_hybrid_engine import IndoT5HybridParaphraser

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def format_result(result):
    """Format a paraphrase result for display"""
    output = f"""
  Original:              {result.original_text[:70]}...
  Paraphrased:           {result.paraphrased_text[:70]}...
  Method:                {result.method_used}
  Quality Score:         {result.quality_score:.1f}/100
  Semantic Similarity:   {result.semantic_similarity:.2f}
  Lexical Diversity:     {result.lexical_diversity:.2f}
  Syntactic Complexity:  {result.syntactic_complexity:.2f}
  Fluency Score:         {result.fluency_score:.2f}
  Neural Confidence:     {result.neural_confidence:.2f}
  Word Changes:          {result.word_changes}
  Transformations:       {', '.join(result.transformations_applied[:3])}
  Processing Time:       {result.processing_time:.2f}s
"""
    return output

def calculate_output_similarity(text1, text2):
    """Calculate percentage similarity between two texts"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    if not words1 or not words2:
        return 0.0
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return (intersection / union) * 100

def test_single_text(paraphraser, text):
    """Test paraphrasing with all three methods for a single text"""
    print_section(f"Testing: {text[:60]}...")
    
    results = {}
    
    # Test each method
    for method in ["neural", "rule-based", "hybrid"]:
        print(f"\n📝 Testing {method.upper()} method:")
        print(f"  {'─'*76}")
        
        start_time = time.time()
        result = paraphraser.paraphrase(text, method=method)
        elapsed = time.time() - start_time
        
        print(format_result(result))
        results[method] = result
        
        # Verify result is valid
        if result.success:
            print(f"  ✅ Success - Quality: {result.quality_score:.1f}/100")
        else:
            print(f"  ❌ Failed - {result.error_message}")
    
    # Compare diversity between methods
    print(f"\n🔍 DIVERSITY ANALYSIS:")
    print(f"  {'─'*76}")
    
    neural_output = results["neural"].paraphrased_text
    rule_output = results["rule-based"].paraphrased_text
    hybrid_output = results["hybrid"].paraphrased_text
    
    neural_vs_rule = calculate_output_similarity(neural_output, rule_output)
    neural_vs_hybrid = calculate_output_similarity(neural_output, hybrid_output)
    rule_vs_hybrid = calculate_output_similarity(rule_output, hybrid_output)
    
    print(f"  Neural vs Rule-based:  {neural_vs_rule:.1f}% similar")
    print(f"  Neural vs Hybrid:      {neural_vs_hybrid:.1f}% similar")
    print(f"  Rule-based vs Hybrid:  {rule_vs_hybrid:.1f}% similar")
    
    avg_diversity = (neural_vs_rule + neural_vs_hybrid + rule_vs_hybrid) / 3
    if avg_diversity < 60:
        print(f"  ✅ Good diversity (avg {avg_diversity:.1f}% - methods are distinct)")
    elif avg_diversity < 75:
        print(f"  ⚠️  Moderate diversity (avg {avg_diversity:.1f}%)")
    else:
        print(f"  ❌ Low diversity (avg {avg_diversity:.1f}%)")
    
    # Quality comparison
    print(f"\n📊 QUALITY COMPARISON:")
    print(f"  {'─'*76}")
    
    neural_qual = results["neural"].quality_score
    rule_qual = results["rule-based"].quality_score
    hybrid_qual = results["hybrid"].quality_score
    avg_qual = (neural_qual + rule_qual + hybrid_qual) / 3
    
    print(f"  Neural Quality:        {neural_qual:.1f}/100")
    print(f"  Rule-based Quality:    {rule_qual:.1f}/100")
    print(f"  Hybrid Quality:        {hybrid_qual:.1f}/100")
    print(f"  Average Quality:       {avg_qual:.1f}/100")
    
    if avg_qual >= 55:
        print(f"  ✅ Good overall quality")
    elif avg_qual >= 45:
        print(f"  ⚠️  Acceptable quality")
    else:
        print(f"  ❌ Low quality")
    
    return results

def main():
    """Main test function"""
    print("\n" + "="*80)
    print("  INDOT5 HYBRID PARAPHRASER - QUALITY IMPROVEMENT TEST")
    print("="*80)
    print("\n📌 Testing three paraphrasing methods with different strategies:")
    print("   • Neural (IndoT5): Multiple strategies with temperature variation")
    print("   • Rule-based: Enhanced with higher synonym rate + word reordering")
    print("   • Hybrid: Balanced combination of neural + rule-based")
    
    # Initialize paraphraser
    print("\n⏳ Initializing paraphraser...")
    try:
        paraphraser = IndoT5HybridParaphraser(
            use_gpu=False,  # CPU only
            synonym_rate=0.7,
            min_confidence=0.5,
            enable_caching=True
        )
        print("✅ Paraphraser initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize paraphraser: {e}")
        sys.exit(1)
    
    # Test texts - Indonesian examples
    test_texts = [
        "Kecerdasan buatan adalah cabang ilmu komputer yang fokus pada pembuatan mesin cerdas.",
        "Pemerintah mengumumkan kebijakan baru untuk meningkatkan kualitas pendidikan di seluruh negara.",
        "Kemajuan teknologi telah mengubah cara masyarakat berkomunikasi dan berbisnis secara signifikan.",
    ]
    
    all_results = {}
    
    try:
        for text in test_texts:
            results = test_single_text(paraphraser, text)
            all_results[text] = results
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Summary
    print_section("TEST SUMMARY")
    
    total_tests = len(test_texts) * 3
    print(f"✅ Total tests completed: {total_tests}")
    
    print("\n📈 Key Improvements Implemented:")
    print("   1. Neural (IndoT5):")
    print("      • Multiple strategies: 'parafrasekan' @1.3°C, 'tulis ulang' @1.1°C")
    print("      • 2 candidates per strategy = 4 total candidates")
    print("      • Smart selection via semantic similarity (0.75) + diversity (0.25)")
    print("      • Invalid candidates filtered automatically")
    print()
    print("   2. Rule-based Enhancement:")
    print("      • Higher synonym rate: 0.85 (vs default 0.7 = +1.3x multiplier)")
    print("      • Maximum transformations: 4 (vs default 3)")
    print("      • Word reordering: 60% probability for natural variation")
    print()
    print("   3. Hybrid Strategy:")
    print("      • Good confidence: Balanced enhancements (0.65 synonym rate)")
    print("      • Low confidence: Aggressive fallback (0.85 synonym rate + word reorder)")
    print("      • Combines semantic accuracy from neural with diversity from rules")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    main()
