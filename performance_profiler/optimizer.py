"""
Auto-optimization suggestion engine.
"""

import ast
import inspect
from typing import List, Dict, Any, Tuple
import re


class OptimizationSuggestion:
    """Represents a single optimization suggestion."""
    
    def __init__(self, line_no: int, issue: str, suggestion: str, 
                 impact: str, code_snippet: str = ""):
        self.line_no = line_no
        self.issue = issue
        self.suggestion = suggestion
        self.impact = impact  # "high", "medium", "low"
        self.code_snippet = code_snippet
    
    def __repr__(self):
        return f"<OptimizationSuggestion line={self.line_no} impact={self.impact}>"


class OptimizerEngine:
    """AI-powered optimization suggestion engine."""
    
    def __init__(self):
        self.suggestions = []
        self._rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[Dict[str, Any]]:
        """Initialize optimization rules."""
        return [
            {
                'name': 'list_comprehension',
                'pattern': r'for\s+\w+\s+in\s+.*:\s*\w+\.append\(',
                'issue': 'Using append in loop',
                'suggestion': 'Replace with list comprehension for better performance',
                'impact': 'medium'
            },
            {
                'name': 'string_concatenation',
                'pattern': r'\w+\s*\+=\s*["\']',
                'issue': 'String concatenation in loop',
                'suggestion': 'Use str.join() or list accumulation instead',
                'impact': 'high'
            },
            {
                'name': 'repeated_function_calls',
                'pattern': r'(len|range)\([^)]+\)',
                'issue': 'Function called multiple times',
                'suggestion': 'Cache function result in variable',
                'impact': 'low'
            },
            {
                'name': 'global_lookup',
                'pattern': r'\bglobal\s+\w+',
                'issue': 'Global variable access',
                'suggestion': 'Use local variables or pass as parameters',
                'impact': 'medium'
            },
            {
                'name': 'nested_loops',
                'pattern': r'for\s+.*:\s*for\s+',
                'issue': 'Nested loops detected',
                'suggestion': 'Consider algorithmic improvements or vectorization',
                'impact': 'high'
            }
        ]
    
    def analyze_code(self, code: str) -> List[OptimizationSuggestion]:
        """
        Analyze code and generate optimization suggestions.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        lines = code.split('\n')
        
        # Pattern-based analysis
        for line_no, line in enumerate(lines, 1):
            for rule in self._rules:
                if re.search(rule['pattern'], line, re.IGNORECASE):
                    suggestions.append(OptimizationSuggestion(
                        line_no=line_no,
                        issue=rule['issue'],
                        suggestion=rule['suggestion'],
                        impact=rule['impact'],
                        code_snippet=line.strip()
                    ))
        
        # AST-based analysis
        try:
            tree = ast.parse(code)
            ast_suggestions = self._analyze_ast(tree, lines)
            suggestions.extend(ast_suggestions)
        except SyntaxError:
            pass  # Skip if code has syntax errors
        
        return suggestions
    
    def _analyze_ast(self, tree: ast.AST, lines: List[str]) -> List[OptimizationSuggestion]:
        """
        Perform AST-based code analysis.
        
        Args:
            tree: AST tree
            lines: Source code lines
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        for node in ast.walk(tree):
            # Check for inefficient operations
            if isinstance(node, ast.For):
                # Check for nested loops
                for inner_node in ast.walk(node):
                    if isinstance(inner_node, ast.For) and inner_node != node:
                        suggestions.append(OptimizationSuggestion(
                            line_no=node.lineno,
                            issue='Deeply nested loops',
                            suggestion='Consider flattening or using itertools.product()',
                            impact='high',
                            code_snippet=lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                        ))
                        break
            
            # Check for list/dict operations in loops
            elif isinstance(node, ast.Call):
                if hasattr(node.func, 'attr'):
                    if node.func.attr in ['append', 'extend']:
                        # Check if inside a loop
                        suggestions.append(OptimizationSuggestion(
                            line_no=node.lineno,
                            issue='List modification in loop',
                            suggestion='Consider using list comprehension or map()',
                            impact='medium',
                            code_snippet=lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ""
                        ))
        
        return suggestions
    
    def analyze_function(self, func) -> List[OptimizationSuggestion]:
        """
        Analyze a function and provide suggestions.
        
        Args:
            func: Function object to analyze
            
        Returns:
            List of optimization suggestions
        """
        try:
            source = inspect.getsource(func)
            return self.analyze_code(source)
        except (OSError, TypeError):
            return []
    
    def suggest_from_profile(self, profile_data: Dict[str, Any], 
                            threshold_time: float = 0.01,
                            threshold_memory: float = 10.0) -> List[OptimizationSuggestion]:
        """
        Generate suggestions based on profiling data.
        
        Args:
            profile_data: Profiling results dictionary
            threshold_time: Time threshold in seconds
            threshold_memory: Memory threshold in MB
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        for func_name, stats in profile_data.items():
            # Time-based suggestions
            if 'total_time' in stats and stats['total_time'] > threshold_time:
                avg_time = stats['total_time'] / stats.get('calls', 1)
                if avg_time > threshold_time:
                    suggestions.append(OptimizationSuggestion(
                        line_no=0,
                        issue=f"Function '{func_name}' is slow",
                        suggestion=f"Average execution time: {avg_time:.4f}s. Consider optimization or caching.",
                        impact='high',
                        code_snippet=func_name
                    ))
            
            # Memory-based suggestions
            if 'peak_memory' in stats and stats['peak_memory'] > threshold_memory:
                suggestions.append(OptimizationSuggestion(
                    line_no=0,
                    issue=f"Function '{func_name}' uses high memory",
                    suggestion=f"Peak memory: {stats['peak_memory']:.2f}MB. Consider generators or chunking.",
                    impact='high',
                    code_snippet=func_name
                ))
            
            # Call frequency suggestions
            if 'calls' in stats and stats['calls'] > 1000:
                suggestions.append(OptimizationSuggestion(
                    line_no=0,
                    issue=f"Function '{func_name}' called {stats['calls']} times",
                    suggestion="Consider caching results with functools.lru_cache",
                    impact='medium',
                    code_snippet=func_name
                ))
        
        return suggestions
    
    def print_suggestions(self, suggestions: List[OptimizationSuggestion]):
        """
        Print optimization suggestions in a formatted manner.
        
        Args:
            suggestions: List of suggestions to print
        """
        if not suggestions:
            print("✅ No optimization suggestions - code looks good!")
            return
        
        print("\n" + "="*80)
        print("💡 Auto-Optimization Suggestions")
        print("="*80)
        
        # Group by impact
        high_impact = [s for s in suggestions if s.impact == 'high']
        medium_impact = [s for s in suggestions if s.impact == 'medium']
        low_impact = [s for s in suggestions if s.impact == 'low']
        
        for category, items in [
            ('🔴 HIGH IMPACT', high_impact),
            ('🟡 MEDIUM IMPACT', medium_impact),
            ('🟢 LOW IMPACT', low_impact)
        ]:
            if items:
                print(f"\n{category}:")
                print("-" * 80)
                for idx, sugg in enumerate(items, 1):
                    print(f"\n{idx}. Line {sugg.line_no if sugg.line_no > 0 else 'N/A'}")
                    print(f"   Issue: {sugg.issue}")
                    print(f"   Suggestion: {sugg.suggestion}")
                    if sugg.code_snippet:
                        print(f"   Code: {sugg.code_snippet[:70]}")
        
        print("\n" + "="*80)
        print(f"Total suggestions: {len(suggestions)}")
        print("="*80)
    
    def generate_report(self, suggestions: List[OptimizationSuggestion]) -> str:
        """
        Generate a text report of suggestions.
        
        Args:
            suggestions: List of suggestions
            
        Returns:
            Formatted report string
        """
        if not suggestions:
            return "No optimization suggestions."
        
        report = ["OPTIMIZATION REPORT", "=" * 50, ""]
        
        for idx, sugg in enumerate(suggestions, 1):
            report.append(f"{idx}. {sugg.issue}")
            report.append(f"   Line: {sugg.line_no}")
            report.append(f"   Impact: {sugg.impact.upper()}")
            report.append(f"   Suggestion: {sugg.suggestion}")
            report.append("")
        
        return "\n".join(report)
