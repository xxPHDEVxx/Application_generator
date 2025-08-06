"""
Text processing utilities for managing token limits.
"""

from typing import Tuple

class TextProcessor:
    """
    Handles text truncation and token management for LLM inputs.
    """
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Estimate the number of tokens in a text.
        
        Args:
            text: The text to count tokens for
            
        Returns:
            int: Estimated token count
        """
        # Approximation (1 token ≈ 4 characters)
        return len(text) // 4
    
    @staticmethod
    def truncate_text(text: str, max_chars: int, preserve_end: bool = False) -> str:
        """
        Truncate text to a maximum character length.
        
        Args:
            text: The text to truncate
            max_chars: Maximum number of characters
            preserve_end: If True, preserve the end of the text instead of the beginning
            
        Returns:
            str: Truncated text
        """
        if len(text) <= max_chars:
            return text
        
        if preserve_end:
            return "..." + text[-(max_chars - 3):]
        else:
            return text[:max_chars - 3] + "..."
    
    @staticmethod
    def smart_truncate_cv(cv_text: str, max_chars: int = 3000) -> str:
        """
        Intelligently truncate CV text, prioritizing recent experience.
        
        Args:
            cv_text: Full CV text
            max_chars: Maximum character count
            
        Returns:
            str: Truncated CV focusing on most relevant parts
        """
        if len(cv_text) <= max_chars:
            return cv_text
        
        lines = cv_text.split('\n')
        
        # Try to identify and preserve key sections
        important_keywords = ['experience', 'work', 'skills', 'education', 'projects']
        important_sections = []
        current_section = []
        in_important = False
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if this line starts an important section
            if any(keyword in line_lower for keyword in important_keywords):
                if current_section and in_important:
                    important_sections.append('\n'.join(current_section))
                current_section = [line]
                in_important = True
            elif in_important:
                current_section.append(line)
                
                # Check if we've reached the character limit
                current_text = '\n'.join(important_sections + ['\n'.join(current_section)])
                if len(current_text) > max_chars:
                    break
        
        # Add the last section if within limits
        if current_section and in_important:
            important_sections.append('\n'.join(current_section))
        
        result = '\n'.join(important_sections)
        
        # If still too long or too short, use simple truncation
        if len(result) > max_chars:
            result = result[:max_chars - 3] + "..."
        elif len(result) < max_chars // 2:
            # If we didn't capture enough, just truncate the original
            result = cv_text[:max_chars - 3] + "..."
        
        return result
    
    @staticmethod
    def smart_truncate_job(job_text: str, max_chars: int = 2000) -> str:
        """
        Intelligently truncate job description, focusing on requirements and responsibilities.
        
        Args:
            job_text: Full job description text
            max_chars: Maximum character count
            
        Returns:
            str: Truncated job description focusing on key parts
        """
        if len(job_text) <= max_chars:
            return job_text
        
        lines = job_text.split('\n')
        
        # Prioritize these sections
        priority_keywords = ['requirements', 'responsibilities', 'qualifications', 'skills', 
                           'experience', 'duties', 'role', 'position', 'about']
        
        important_lines = []
        other_lines = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in priority_keywords):
                important_lines.append(line)
            else:
                other_lines.append(line)
        
        # Build result prioritizing important lines
        result = '\n'.join(important_lines)
        
        # Add other lines if space permits
        for line in other_lines:
            if len(result) + len(line) + 1 < max_chars:
                result += '\n' + line
            else:
                break
        
        if len(result) > max_chars:
            result = result[:max_chars - 3] + "..."
        
        return result
    
    @staticmethod
    def prepare_for_llm(cv_text: str, job_text: str, max_total_chars: int = 5000) -> Tuple[str, str]:
        """
        Prepare CV and job description for LLM input, ensuring they fit within token limits.
        
        Args:
            cv_text: Full CV text
            job_text: Full job description
            max_total_chars: Maximum total characters (approximately 1250 tokens)
            
        Returns:
            Tuple[str, str]: Truncated CV and job description
        """
        # Allocate 60% to CV, 40% to job description
        cv_max = int(max_total_chars * 0.6)
        job_max = int(max_total_chars * 0.4)
        
        # Smart truncation
        truncated_cv = TextProcessor.smart_truncate_cv(cv_text, cv_max)
        truncated_job = TextProcessor.smart_truncate_job(job_text, job_max)
        
        return truncated_cv, truncated_job