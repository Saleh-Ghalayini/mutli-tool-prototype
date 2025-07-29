"""
Summarization Service - Handles document summarization logic
"""

from typing import Dict, Any
from services.pdf_service import PDFService
from services.ai_service import AIService
from services.prompt_service import PromptService, PromptType
from services.file_service import FileService

class SummarizationService:
    """Service for document summarization operations"""
    
    def __init__(self, ai_service: AIService, file_service: FileService):
        self.ai_service = ai_service
        self.file_service = file_service
        self.pdf_service = PDFService()
    
    def summarize_pdf(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize a PDF document"""
        # Validate request
        file_path = request.get("file_path")
        if not file_path:
            return {
                "summary": "",
                "success": False,
                "error": "file_path is required"
            }
        
        try:
            # Extract PDF text
            pdf_text = self.pdf_service.extract_text_from_file(file_path)
            
            if not pdf_text.strip():
                return {
                    "summary": "",
                    "success": False,
                    "error": "No text could be extracted from the PDF"
                }
            
            original_length = len(pdf_text)
            summary_length = request.get("summary_length", "medium")
            
            # Generate prompt
            prompt = PromptService.get_prompt(
                PromptType.PDF_SUMMARIZATION,
                summary_length=summary_length,
                document_text=pdf_text
            )
            
            # Generate summary
            max_tokens_map = {
                "short": 150,
                "medium": 300, 
                "long": 600
            }
            max_tokens = max_tokens_map.get(summary_length, 300)
            
            stop_sequences = [
                "\n\nDOCUMENT:", "EXAMPLES:", "FORMAT RULES:", "TASK:", 
                "Example", "\n\nEXAMPLE", "Write a comprehensive", "\n\nWrite"
            ]
            
            raw_summary = self.ai_service.generate_text(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.2,
                top_p=0.9,
                stop_sequences=stop_sequences
            )
            
            # Post-process summary
            summary = self._post_process_summary(raw_summary, summary_length)
            
            # Validate summary
            validation_result = self._validate_summary(summary)
            if not validation_result["valid"]:
                return {
                    "summary": "",
                    "success": False,
                    "error": validation_result["error"]
                }
            
            # Clean up temp file
            self.file_service.cleanup_file(file_path)
            
            return {
                "summary": summary,
                "success": True,
                "original_length": original_length,
                "summary_length": len(summary),
                "compression_ratio": None,
                "strategy_used": None,
                "processing_type": None
            }
            
        except Exception as e:
            # Clean up temp file on error
            self.file_service.cleanup_file(file_path)
            return {
                "summary": "",
                "success": False,
                "error": str(e)
            }
    
    def _post_process_summary(self, raw_summary: str, summary_length: str) -> str:
        """Post-process the raw summary to clean up artifacts"""
        summary = raw_summary
        
        # Remove prompt artifacts
        summary = summary.replace("SUMMARY:", "").strip()
        summary = summary.replace("Summary:", "").strip()
        summary = summary.replace("Write a comprehensive summary", "").strip()
        
        # Clean up line by line
        lines = summary.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip example content and section headers
            if (line.startswith("Example") or line.startswith("EXAMPLE") or 
                line.startswith("PROFESSIONAL") or line.startswith("EDUCATIONAL") or
                line.startswith("Write a comprehensive") or not line):
                continue
            
            # Skip lines with prompt artifacts
            if not any(skip_word in line.lower() for skip_word in ["example", "format rules", "document to summarize"]):
                cleaned_lines.append(line)
        
        summary = '\n'.join(cleaned_lines).strip()
        
        # Clean up remaining artifacts
        summary = summary.replace("that captures all essential information in a natural, flowing narrative:", "").strip()
        
        # Format long summaries into paragraphs
        if summary_length == "long" and summary:
            sentences = summary.split('. ')
            if len(sentences) > 6:
                mid_point = len(sentences) // 2
                paragraph1 = '. '.join(sentences[:mid_point]) + '.'
                paragraph2 = '. '.join(sentences[mid_point:])
                if not paragraph2.endswith('.'):
                    paragraph2 += '.'
                summary = paragraph1 + '\n\n' + paragraph2
        
        # Ensure proper sentence ending
        if summary and not summary.endswith(('.', '!', '?')):
            sentences = summary.split('.')
            if len(sentences) > 1:
                summary = '.'.join(sentences[:-1]) + '.'
        
        return summary
    
    def _validate_summary(self, summary: str) -> Dict[str, Any]:
        """Validate summary quality and detect common errors"""
        if len(summary) < 20:
            return {
                "valid": False,
                "error": "Generated summary too short or low quality. Please try again."
            }
        
        # Check for hallucination patterns
        error_patterns = [
            ("42 years", "Detected potential confusion between '42 School' and years of experience"),
            ("decades of experience", "Detected unrealistic experience duration"),
            ("veteran engineer", "Detected age-related assumption not in document")
        ]
        
        for pattern, error_msg in error_patterns:
            if pattern in summary.lower():
                return {
                    "valid": False,
                    "error": error_msg + ". Please regenerate."
                }
        
        return {"valid": True, "error": None}
