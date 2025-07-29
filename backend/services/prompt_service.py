"""
Prompt Service - Centralized prompt management for different AI tools
Provides specialized prompts for different use cases (summarization, chat, etc.)
"""

from typing import Dict, Any, Optional
from enum import Enum

class PromptType(Enum):
    """Enum for different prompt types"""
    PDF_SUMMARIZATION = "pdf_summarization"

class PromptService:
    """Service for managing and providing AI prompts based on tool type"""
    
    @staticmethod
    def get_prompt(prompt_type: PromptType, **kwargs) -> str:
        """
        Get the appropriate prompt based on the tool type and parameters
        
        Args:
            prompt_type: The type of prompt needed
            **kwargs: Additional parameters for prompt customization
            
        Returns:
            str: The formatted prompt string
        """
        if prompt_type == PromptType.PDF_SUMMARIZATION:
            return PromptService._get_pdf_summarization_prompt(**kwargs)
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    @staticmethod
    def _get_pdf_summarization_prompt(
        summary_length: str = "medium",
        document_text: str = "",
        **kwargs
    ) -> str:
        """Generate a specialized prompt for PDF summarization"""
        
        return f"""You are a professional document analyst and expert summarizer with years of experience in extracting key information from complex documents.

TASK: Create a comprehensive, well-structured summary of the provided document text.

REQUIREMENTS:
- Length: {summary_length} (short=2-3 sentences, medium=1 paragraph, long=2-3 paragraphs)
- Include ALL key information without omitting important details
- Use clear, professional language maintaining the document's tone
- Maintain complete factual accuracy - do not add information not in the document
- Present information in logical, flowing narrative form
- DO NOT confuse institution/school names with years of experience
- NEVER invent dates, durations, or quantitative data not explicitly stated

FORMAT RULES:
1. Write as a cohesive narrative summary (no section headers or artificial breaks)
2. Include key entities, concepts, findings, or achievements with specific details
3. Include relevant dates, locations, technologies, and quantifiable data when mentioned
4. Use complete sentences with smooth transitions between topics
5. End naturally without abrupt cutoffs or additional commentary
6. Maintain the document's original context and purpose

EXAMPLES:

Example 1 (Professional Document - Short):
The quarterly report shows company revenue increased 15% to $2.3 million, driven primarily by new client acquisitions in the healthcare sector. The engineering team successfully deployed three major product updates, improving system performance by 40%.

Example 2 (Research/Academic Document - Long):
This comprehensive study examines the impact of remote work policies on employee productivity across 500 technology companies during 2020-2022. The research utilized mixed-method analysis including surveys of 15,000 employees and performance data from HR systems, revealing a 23% average increase in productivity when employees work remotely 3-4 days per week. The findings indicate highest productivity gains in creative and analytical roles, while collaborative tasks showed minimal impact. The study recommends hybrid work models as optimal for both employee satisfaction and organizational performance.

Example 3 (Technical Document):
The system architecture utilizes microservices deployed on AWS with Docker containerization, supporting up to 10,000 concurrent users through load-balanced instances. Key technologies include React frontend, Node.js APIs, PostgreSQL database, and Redis caching, with automated CI/CD pipelines ensuring 99.9% uptime across production environments.

DOCUMENT TO SUMMARIZE:
{document_text[:4000]}

Write a comprehensive summary that captures all essential information in a natural, flowing narrative:"""
