MATCH (n) DETACH DELETE n;

// ----------------------------------------------------------------------------
// PART 1: CREATE 30 DIVERSE AGENTS
// ----------------------------------------------------------------------------

// Web & Search Agents
MERGE (a1:Agent {
  name: 'WebSearch Pro',
  description: 'Advanced web search with multi-source aggregation and real-time results',
  capabilityLevel: 0.9,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.85,
  responseTime: 0.3,
  costEfficiency: 0.8,
  reliability: 0.95,
  specializationScore: 0.9,
  successCount: 150,
  failureCount: 25
});

MERGE (a2:Agent {
  name: 'DeepSearch Agent',
  description: 'Deep web search with academic and research database access',
  capabilityLevel: 0.85,
  domainExpertise: 'research',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.80,
  responseTime: 0.5,
  costEfficiency: 0.7,
  reliability: 0.90,
  specializationScore: 0.85,
  successCount: 120,
  failureCount: 30
});

// Code & Development Agents
MERGE (a3:Agent {
  name: 'CodeAnalyzer Pro',
  description: 'Multi-language code analysis with security scanning and performance optimization',
  capabilityLevel: 0.92,
  domainExpertise: 'development',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.88,
  responseTime: 0.4,
  costEfficiency: 0.75,
  reliability: 0.93,
  specializationScore: 0.92,
  successCount: 200,
  failureCount: 25
});

MERGE (a4:Agent {
  name: 'CodeGenerator AI',
  description: 'Intelligent code generation from natural language descriptions',
  capabilityLevel: 0.87,
  domainExpertise: 'development',
  inputFormat: 'text',
  outputFormat: 'code',
  historicalAccuracy: 0.82,
  responseTime: 0.6,
  costEfficiency: 0.70,
  reliability: 0.88,
  specializationScore: 0.87,
  successCount: 180,
  failureCount: 40
});

MERGE (a5:Agent {
  name: 'DebugMaster',
  description: 'Automated debugging and error resolution for multiple programming languages',
  capabilityLevel: 0.89,
  domainExpertise: 'development',
  inputFormat: 'code',
  outputFormat: 'text',
  historicalAccuracy: 0.85,
  responseTime: 0.5,
  costEfficiency: 0.72,
  reliability: 0.91,
  specializationScore: 0.89,
  successCount: 170,
  failureCount: 30
});

// Document & Text Agents
MERGE (a6:Agent {
  name: 'DocumentSummarizer',
  description: 'Intelligent document summarization with key point extraction',
  capabilityLevel: 0.88,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.86,
  responseTime: 0.4,
  costEfficiency: 0.78,
  reliability: 0.92,
  specializationScore: 0.88,
  successCount: 160,
  failureCount: 25
});

MERGE (a7:Agent {
  name: 'TextAnalyzer Pro',
  description: 'Advanced text analysis with sentiment, entity extraction, and topic modeling',
  capabilityLevel: 0.85,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.83,
  responseTime: 0.45,
  costEfficiency: 0.75,
  reliability: 0.89,
  specializationScore: 0.85,
  successCount: 140,
  failureCount: 30
});

MERGE (a8:Agent {
  name: 'TranslationMaster',
  description: 'Multi-language translation with context awareness and cultural adaptation',
  capabilityLevel: 0.90,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.87,
  responseTime: 0.35,
  costEfficiency: 0.80,
  reliability: 0.94,
  specializationScore: 0.90,
  successCount: 220,
  failureCount: 30
});

// Data & Analytics Agents
MERGE (a9:Agent {
  name: 'DataAnalyzer Pro',
  description: 'Comprehensive data analysis with statistical modeling and visualization',
  capabilityLevel: 0.91,
  domainExpertise: 'analytics',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.89,
  responseTime: 0.5,
  costEfficiency: 0.73,
  reliability: 0.92,
  specializationScore: 0.91,
  successCount: 190,
  failureCount: 25
});

MERGE (a10:Agent {
  name: 'ChartGenerator',
  description: 'Intelligent chart and graph generation from data with automatic best-fit visualization',
  capabilityLevel: 0.86,
  domainExpertise: 'analytics',
  inputFormat: 'json',
  outputFormat: 'image',
  historicalAccuracy: 0.84,
  responseTime: 0.4,
  costEfficiency: 0.77,
  reliability: 0.90,
  specializationScore: 0.86,
  successCount: 155,
  failureCount: 30
});

MERGE (a11:Agent {
  name: 'PredictiveAnalytics',
  description: 'Machine learning-based predictive analytics and forecasting',
  capabilityLevel: 0.93,
  domainExpertise: 'analytics',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.87,
  responseTime: 0.7,
  costEfficiency: 0.65,
  reliability: 0.91,
  specializationScore: 0.93,
  successCount: 175,
  failureCount: 25
});

// Content & Creative Agents
MERGE (a12:Agent {
  name: 'ContentWriter Pro',
  description: 'AI-powered content writing with SEO optimization and tone adaptation',
  capabilityLevel: 0.88,
  domainExpertise: 'content',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.85,
  responseTime: 0.5,
  costEfficiency: 0.76,
  reliability: 0.91,
  specializationScore: 0.88,
  successCount: 200,
  failureCount: 35
});

MERGE (a13:Agent {
  name: 'CreativeAssistant',
  description: 'Creative writing and brainstorming with style and genre adaptation',
  capabilityLevel: 0.84,
  domainExpertise: 'content',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.81,
  responseTime: 0.6,
  costEfficiency: 0.74,
  reliability: 0.87,
  specializationScore: 0.84,
  successCount: 165,
  failureCount: 40
});

MERGE (a14:Agent {
  name: 'ImageGenerator',
  description: 'AI image generation from text descriptions with style control',
  capabilityLevel: 0.87,
  domainExpertise: 'content',
  inputFormat: 'text',
  outputFormat: 'image',
  historicalAccuracy: 0.83,
  responseTime: 0.8,
  costEfficiency: 0.68,
  reliability: 0.89,
  specializationScore: 0.87,
  successCount: 180,
  failureCount: 35
});

// Communication & Interaction Agents
MERGE (a15:Agent {
  name: 'ChatBot Pro',
  description: 'Intelligent conversational AI with context retention and personality',
  capabilityLevel: 0.89,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.86,
  responseTime: 0.3,
  costEfficiency: 0.79,
  reliability: 0.93,
  specializationScore: 0.89,
  successCount: 250,
  failureCount: 40
});

MERGE (a16:Agent {
  name: 'EmailAssistant',
  description: 'Email composition, summarization, and intelligent response generation',
  capabilityLevel: 0.86,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.84,
  responseTime: 0.35,
  costEfficiency: 0.78,
  reliability: 0.90,
  specializationScore: 0.86,
  successCount: 195,
  failureCount: 35
});

// Specialized Domain Agents
MERGE (a17:Agent {
  name: 'LegalAnalyzer',
  description: 'Legal document analysis, contract review, and compliance checking',
  capabilityLevel: 0.90,
  domainExpertise: 'legal',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.88,
  responseTime: 0.6,
  costEfficiency: 0.71,
  reliability: 0.92,
  specializationScore: 0.90,
  successCount: 145,
  failureCount: 20
});

MERGE (a18:Agent {
  name: 'MedicalResearch',
  description: 'Medical literature search, evidence synthesis, and research assistance',
  capabilityLevel: 0.91,
  domainExpertise: 'medical',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.89,
  responseTime: 0.7,
  costEfficiency: 0.69,
  reliability: 0.93,
  specializationScore: 0.91,
  successCount: 130,
  failureCount: 15
});

MERGE (a19:Agent {
  name: 'FinancialAnalyst',
  description: 'Financial data analysis, market trend prediction, and risk assessment',
  capabilityLevel: 0.92,
  domainExpertise: 'finance',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.90,
  responseTime: 0.5,
  costEfficiency: 0.72,
  reliability: 0.94,
  specializationScore: 0.92,
  successCount: 160,
  failureCount: 18
});

MERGE (a20:Agent {
  name: 'EducationalTutor',
  description: 'Personalized educational assistance with adaptive learning and explanations',
  capabilityLevel: 0.87,
  domainExpertise: 'education',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.85,
  responseTime: 0.4,
  costEfficiency: 0.77,
  reliability: 0.91,
  specializationScore: 0.87,
  successCount: 210,
  failureCount: 35
});

// Media & Audio Agents
MERGE (a21:Agent {
  name: 'AudioTranscriber',
  description: 'High-accuracy audio transcription with speaker identification and timestamps',
  capabilityLevel: 0.88,
  domainExpertise: 'media',
  inputFormat: 'audio',
  outputFormat: 'text',
  historicalAccuracy: 0.86,
  responseTime: 0.6,
  costEfficiency: 0.74,
  reliability: 0.90,
  specializationScore: 0.88,
  successCount: 175,
  failureCount: 28
});

MERGE (a22:Agent {
  name: 'VideoAnalyzer',
  description: 'Video content analysis with scene detection, object recognition, and transcription',
  capabilityLevel: 0.89,
  domainExpertise: 'media',
  inputFormat: 'video',
  outputFormat: 'json',
  historicalAccuracy: 0.87,
  responseTime: 0.8,
  costEfficiency: 0.66,
  reliability: 0.91,
  specializationScore: 0.89,
  successCount: 140,
  failureCount: 20
});

// Security & Quality Agents
MERGE (a23:Agent {
  name: 'SecurityScanner',
  description: 'Comprehensive security scanning for code, networks, and systems',
  capabilityLevel: 0.93,
  domainExpertise: 'security',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.91,
  responseTime: 0.5,
  costEfficiency: 0.70,
  reliability: 0.95,
  specializationScore: 0.93,
  successCount: 185,
  failureCount: 18
});

MERGE (a24:Agent {
  name: 'QualityAssurance',
  description: 'Automated quality assurance testing and validation for software and content',
  capabilityLevel: 0.90,
  domainExpertise: 'development',
  inputFormat: 'code',
  outputFormat: 'json',
  historicalAccuracy: 0.88,
  responseTime: 0.45,
  costEfficiency: 0.75,
  reliability: 0.92,
  specializationScore: 0.90,
  successCount: 195,
  failureCount: 25
});

// Automation & Workflow Agents
MERGE (a25:Agent {
  name: 'WorkflowAutomator',
  description: 'Intelligent workflow automation with multi-step process orchestration',
  capabilityLevel: 0.91,
  domainExpertise: 'automation',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.89,
  responseTime: 0.4,
  costEfficiency: 0.73,
  reliability: 0.93,
  specializationScore: 0.91,
  successCount: 170,
  failureCount: 20
});

MERGE (a26:Agent {
  name: 'APIIntegrator',
  description: 'API integration and orchestration with error handling and retry logic',
  capabilityLevel: 0.88,
  domainExpertise: 'development',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.86,
  responseTime: 0.35,
  costEfficiency: 0.78,
  reliability: 0.91,
  specializationScore: 0.88,
  successCount: 200,
  failureCount: 30
});

// Research & Analysis Agents
MERGE (a27:Agent {
  name: 'ResearchAssistant',
  description: 'Comprehensive research assistance with multi-source synthesis and citation',
  capabilityLevel: 0.89,
  domainExpertise: 'research',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.87,
  responseTime: 0.6,
  costEfficiency: 0.71,
  reliability: 0.92,
  specializationScore: 0.89,
  successCount: 155,
  failureCount: 23
});

MERGE (a28:Agent {
  name: 'FactChecker',
  description: 'Automated fact-checking with source verification and credibility assessment',
  capabilityLevel: 0.87,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'json',
  historicalAccuracy: 0.85,
  responseTime: 0.5,
  costEfficiency: 0.76,
  reliability: 0.90,
  specializationScore: 0.87,
  successCount: 165,
  failureCount: 30
});

// Recommendation & Personalization Agents
MERGE (a29:Agent {
  name: 'RecommendationEngine',
  description: 'Personalized recommendation engine with collaborative filtering and ML',
  capabilityLevel: 0.90,
  domainExpertise: 'analytics',
  inputFormat: 'json',
  outputFormat: 'json',
  historicalAccuracy: 0.88,
  responseTime: 0.4,
  costEfficiency: 0.74,
  reliability: 0.92,
  specializationScore: 0.90,
  successCount: 180,
  failureCount: 25
});

MERGE (a30:Agent {
  name: 'FallbackAgent',
  description: 'Universal fallback agent for handling requests when specialized agents fail',
  capabilityLevel: 0.75,
  domainExpertise: 'general',
  inputFormat: 'text',
  outputFormat: 'text',
  historicalAccuracy: 0.70,
  responseTime: 0.5,
  costEfficiency: 0.65,
  reliability: 0.80,
  specializationScore: 0.50,
  successCount: 100,
  failureCount: 45
});

// ----------------------------------------------------------------------------
// PART 2: CREATE FALLBACK_AGENT RELATIONSHIPS
// Every agent must have at least one fallback agent
// ----------------------------------------------------------------------------

// WebSearch Pro fallbacks
MATCH (a1:Agent {name: 'WebSearch Pro'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a1)-[:FALLBACK_AGENT]->(a2);
MATCH (a1:Agent {name: 'WebSearch Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a1)-[:FALLBACK_AGENT]->(a30);

// DeepSearch Agent fallbacks
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a1:Agent {name: 'WebSearch Pro'})
MERGE (a2)-[:FALLBACK_AGENT]->(a1);
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a2)-[:FALLBACK_AGENT]->(a30);

// CodeAnalyzer Pro fallbacks
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a5:Agent {name: 'DebugMaster'})
MERGE (a3)-[:FALLBACK_AGENT]->(a5);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a24:Agent {name: 'QualityAssurance'})
MERGE (a3)-[:FALLBACK_AGENT]->(a24);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a3)-[:FALLBACK_AGENT]->(a30);

// CodeGenerator AI fallbacks
MATCH (a4:Agent {name: 'CodeGenerator AI'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a4)-[:FALLBACK_AGENT]->(a3);
MATCH (a4:Agent {name: 'CodeGenerator AI'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a4)-[:FALLBACK_AGENT]->(a30);

// DebugMaster fallbacks
MATCH (a5:Agent {name: 'DebugMaster'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a5)-[:FALLBACK_AGENT]->(a3);
MATCH (a5:Agent {name: 'DebugMaster'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a5)-[:FALLBACK_AGENT]->(a30);

// DocumentSummarizer fallbacks
MATCH (a6:Agent {name: 'DocumentSummarizer'}), (a7:Agent {name: 'TextAnalyzer Pro'})
MERGE (a6)-[:FALLBACK_AGENT]->(a7);
MATCH (a6:Agent {name: 'DocumentSummarizer'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a6)-[:FALLBACK_AGENT]->(a30);

// TextAnalyzer Pro fallbacks
MATCH (a7:Agent {name: 'TextAnalyzer Pro'}), (a6:Agent {name: 'DocumentSummarizer'})
MERGE (a7)-[:FALLBACK_AGENT]->(a6);
MATCH (a7:Agent {name: 'TextAnalyzer Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a7)-[:FALLBACK_AGENT]->(a30);

// TranslationMaster fallbacks
MATCH (a8:Agent {name: 'TranslationMaster'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a8)-[:FALLBACK_AGENT]->(a15);
MATCH (a8:Agent {name: 'TranslationMaster'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a8)-[:FALLBACK_AGENT]->(a30);

// DataAnalyzer Pro fallbacks
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a11:Agent {name: 'PredictiveAnalytics'})
MERGE (a9)-[:FALLBACK_AGENT]->(a11);
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a9)-[:FALLBACK_AGENT]->(a30);

// ChartGenerator fallbacks
MATCH (a10:Agent {name: 'ChartGenerator'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a10)-[:FALLBACK_AGENT]->(a9);
MATCH (a10:Agent {name: 'ChartGenerator'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a10)-[:FALLBACK_AGENT]->(a30);

// PredictiveAnalytics fallbacks
MATCH (a11:Agent {name: 'PredictiveAnalytics'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a11)-[:FALLBACK_AGENT]->(a9);
MATCH (a11:Agent {name: 'PredictiveAnalytics'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a11)-[:FALLBACK_AGENT]->(a30);

// ContentWriter Pro fallbacks
MATCH (a12:Agent {name: 'ContentWriter Pro'}), (a13:Agent {name: 'CreativeAssistant'})
MERGE (a12)-[:FALLBACK_AGENT]->(a13);
MATCH (a12:Agent {name: 'ContentWriter Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a12)-[:FALLBACK_AGENT]->(a30);

// CreativeAssistant fallbacks
MATCH (a13:Agent {name: 'CreativeAssistant'}), (a12:Agent {name: 'ContentWriter Pro'})
MERGE (a13)-[:FALLBACK_AGENT]->(a12);
MATCH (a13:Agent {name: 'CreativeAssistant'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a13)-[:FALLBACK_AGENT]->(a30);

// ImageGenerator fallbacks
MATCH (a14:Agent {name: 'ImageGenerator'}), (a12:Agent {name: 'ContentWriter Pro'})
MERGE (a14)-[:FALLBACK_AGENT]->(a12);
MATCH (a14:Agent {name: 'ImageGenerator'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a14)-[:FALLBACK_AGENT]->(a30);

// ChatBot Pro fallbacks
MATCH (a15:Agent {name: 'ChatBot Pro'}), (a16:Agent {name: 'EmailAssistant'})
MERGE (a15)-[:FALLBACK_AGENT]->(a16);
MATCH (a15:Agent {name: 'ChatBot Pro'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a15)-[:FALLBACK_AGENT]->(a30);

// EmailAssistant fallbacks
MATCH (a16:Agent {name: 'EmailAssistant'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a16)-[:FALLBACK_AGENT]->(a15);
MATCH (a16:Agent {name: 'EmailAssistant'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a16)-[:FALLBACK_AGENT]->(a30);

// LegalAnalyzer fallbacks
MATCH (a17:Agent {name: 'LegalAnalyzer'}), (a6:Agent {name: 'DocumentSummarizer'})
MERGE (a17)-[:FALLBACK_AGENT]->(a6);
MATCH (a17:Agent {name: 'LegalAnalyzer'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a17)-[:FALLBACK_AGENT]->(a30);

// MedicalResearch fallbacks
MATCH (a18:Agent {name: 'MedicalResearch'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a18)-[:FALLBACK_AGENT]->(a2);
MATCH (a18:Agent {name: 'MedicalResearch'}), (a27:Agent {name: 'ResearchAssistant'})
MERGE (a18)-[:FALLBACK_AGENT]->(a27);
MATCH (a18:Agent {name: 'MedicalResearch'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a18)-[:FALLBACK_AGENT]->(a30);

// FinancialAnalyst fallbacks
MATCH (a19:Agent {name: 'FinancialAnalyst'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a19)-[:FALLBACK_AGENT]->(a9);
MATCH (a19:Agent {name: 'FinancialAnalyst'}), (a11:Agent {name: 'PredictiveAnalytics'})
MERGE (a19)-[:FALLBACK_AGENT]->(a11);
MATCH (a19:Agent {name: 'FinancialAnalyst'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a19)-[:FALLBACK_AGENT]->(a30);

// EducationalTutor fallbacks
MATCH (a20:Agent {name: 'EducationalTutor'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a20)-[:FALLBACK_AGENT]->(a15);
MATCH (a20:Agent {name: 'EducationalTutor'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a20)-[:FALLBACK_AGENT]->(a30);

// AudioTranscriber fallbacks
MATCH (a21:Agent {name: 'AudioTranscriber'}), (a22:Agent {name: 'VideoAnalyzer'})
MERGE (a21)-[:FALLBACK_AGENT]->(a22);
MATCH (a21:Agent {name: 'AudioTranscriber'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a21)-[:FALLBACK_AGENT]->(a30);

// VideoAnalyzer fallbacks
MATCH (a22:Agent {name: 'VideoAnalyzer'}), (a21:Agent {name: 'AudioTranscriber'})
MERGE (a22)-[:FALLBACK_AGENT]->(a21);
MATCH (a22:Agent {name: 'VideoAnalyzer'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a22)-[:FALLBACK_AGENT]->(a30);

// SecurityScanner fallbacks
MATCH (a23:Agent {name: 'SecurityScanner'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a23)-[:FALLBACK_AGENT]->(a3);
MATCH (a23:Agent {name: 'SecurityScanner'}), (a24:Agent {name: 'QualityAssurance'})
MERGE (a23)-[:FALLBACK_AGENT]->(a24);
MATCH (a23:Agent {name: 'SecurityScanner'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a23)-[:FALLBACK_AGENT]->(a30);

// QualityAssurance fallbacks
MATCH (a24:Agent {name: 'QualityAssurance'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a24)-[:FALLBACK_AGENT]->(a3);
MATCH (a24:Agent {name: 'QualityAssurance'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a24)-[:FALLBACK_AGENT]->(a30);

// WorkflowAutomator fallbacks
MATCH (a25:Agent {name: 'WorkflowAutomator'}), (a26:Agent {name: 'APIIntegrator'})
MERGE (a25)-[:FALLBACK_AGENT]->(a26);
MATCH (a25:Agent {name: 'WorkflowAutomator'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a25)-[:FALLBACK_AGENT]->(a30);

// APIIntegrator fallbacks
MATCH (a26:Agent {name: 'APIIntegrator'}), (a25:Agent {name: 'WorkflowAutomator'})
MERGE (a26)-[:FALLBACK_AGENT]->(a25);
MATCH (a26:Agent {name: 'APIIntegrator'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a26)-[:FALLBACK_AGENT]->(a30);

// ResearchAssistant fallbacks
MATCH (a27:Agent {name: 'ResearchAssistant'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a27)-[:FALLBACK_AGENT]->(a2);
MATCH (a27:Agent {name: 'ResearchAssistant'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a27)-[:FALLBACK_AGENT]->(a30);

// FactChecker fallbacks
MATCH (a28:Agent {name: 'FactChecker'}), (a1:Agent {name: 'WebSearch Pro'})
MERGE (a28)-[:FALLBACK_AGENT]->(a1);
MATCH (a28:Agent {name: 'FactChecker'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a28)-[:FALLBACK_AGENT]->(a30);

// RecommendationEngine fallbacks
MATCH (a29:Agent {name: 'RecommendationEngine'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a29)-[:FALLBACK_AGENT]->(a9);
MATCH (a29:Agent {name: 'RecommendationEngine'}), (a30:Agent {name: 'FallbackAgent'})
MERGE (a29)-[:FALLBACK_AGENT]->(a30);

// FallbackAgent fallbacks (can fallback to itself or other general agents)
MATCH (a30:Agent {name: 'FallbackAgent'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a30)-[:FALLBACK_AGENT]->(a15);
MATCH (a30:Agent {name: 'FallbackAgent'}), (a1:Agent {name: 'WebSearch Pro'})
MERGE (a30)-[:FALLBACK_AGENT]->(a1);

// ----------------------------------------------------------------------------
// PART 3: CREATE SIMILAR_TO RELATIONSHIPS
// Agents that perform similar functions
// ----------------------------------------------------------------------------

// Search agents are similar
MATCH (a1:Agent {name: 'WebSearch Pro'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a1)-[:SIMILAR_TO]->(a2);
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a1:Agent {name: 'WebSearch Pro'})
MERGE (a2)-[:SIMILAR_TO]->(a1);

// Code agents are similar
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a4:Agent {name: 'CodeGenerator AI'})
MERGE (a3)-[:SIMILAR_TO]->(a4);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a5:Agent {name: 'DebugMaster'})
MERGE (a3)-[:SIMILAR_TO]->(a5);
MATCH (a4:Agent {name: 'CodeGenerator AI'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a4)-[:SIMILAR_TO]->(a3);
MATCH (a5:Agent {name: 'DebugMaster'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a5)-[:SIMILAR_TO]->(a3);

// Text/document agents are similar
MATCH (a6:Agent {name: 'DocumentSummarizer'}), (a7:Agent {name: 'TextAnalyzer Pro'})
MERGE (a6)-[:SIMILAR_TO]->(a7);
MATCH (a7:Agent {name: 'TextAnalyzer Pro'}), (a6:Agent {name: 'DocumentSummarizer'})
MERGE (a7)-[:SIMILAR_TO]->(a6);

// Content creation agents are similar
MATCH (a12:Agent {name: 'ContentWriter Pro'}), (a13:Agent {name: 'CreativeAssistant'})
MERGE (a12)-[:SIMILAR_TO]->(a13);
MATCH (a13:Agent {name: 'CreativeAssistant'}), (a12:Agent {name: 'ContentWriter Pro'})
MERGE (a13)-[:SIMILAR_TO]->(a12);

// Communication agents are similar
MATCH (a15:Agent {name: 'ChatBot Pro'}), (a16:Agent {name: 'EmailAssistant'})
MERGE (a15)-[:SIMILAR_TO]->(a16);
MATCH (a16:Agent {name: 'EmailAssistant'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a16)-[:SIMILAR_TO]->(a15);

// Analytics agents are similar
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a11:Agent {name: 'PredictiveAnalytics'})
MERGE (a9)-[:SIMILAR_TO]->(a11);
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a19:Agent {name: 'FinancialAnalyst'})
MERGE (a9)-[:SIMILAR_TO]->(a19);
MATCH (a11:Agent {name: 'PredictiveAnalytics'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a11)-[:SIMILAR_TO]->(a9);
MATCH (a19:Agent {name: 'FinancialAnalyst'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a19)-[:SIMILAR_TO]->(a9);

// Media agents are similar
MATCH (a21:Agent {name: 'AudioTranscriber'}), (a22:Agent {name: 'VideoAnalyzer'})
MERGE (a21)-[:SIMILAR_TO]->(a22);
MATCH (a22:Agent {name: 'VideoAnalyzer'}), (a21:Agent {name: 'AudioTranscriber'})
MERGE (a22)-[:SIMILAR_TO]->(a21);

// Research agents are similar
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a27:Agent {name: 'ResearchAssistant'})
MERGE (a2)-[:SIMILAR_TO]->(a27);
MATCH (a18:Agent {name: 'MedicalResearch'}), (a27:Agent {name: 'ResearchAssistant'})
MERGE (a18)-[:SIMILAR_TO]->(a27);
MATCH (a27:Agent {name: 'ResearchAssistant'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a27)-[:SIMILAR_TO]->(a2);

// ----------------------------------------------------------------------------
// PART 4: CREATE COMPLEMENTS RELATIONSHIPS
// Agents that work well together or enhance each other
// ----------------------------------------------------------------------------

// CodeGenerator complements CodeAnalyzer
MATCH (a4:Agent {name: 'CodeGenerator AI'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a4)-[:COMPLEMENTS]->(a3);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a4:Agent {name: 'CodeGenerator AI'})
MERGE (a3)-[:COMPLEMENTS]->(a4);

// DebugMaster complements CodeAnalyzer
MATCH (a5:Agent {name: 'DebugMaster'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a5)-[:COMPLEMENTS]->(a3);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a5:Agent {name: 'DebugMaster'})
MERGE (a3)-[:COMPLEMENTS]->(a5);

// QualityAssurance complements CodeAnalyzer
MATCH (a24:Agent {name: 'QualityAssurance'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a24)-[:COMPLEMENTS]->(a3);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a24:Agent {name: 'QualityAssurance'})
MERGE (a3)-[:COMPLEMENTS]->(a24);

// SecurityScanner complements CodeAnalyzer
MATCH (a23:Agent {name: 'SecurityScanner'}), (a3:Agent {name: 'CodeAnalyzer Pro'})
MERGE (a23)-[:COMPLEMENTS]->(a3);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a23:Agent {name: 'SecurityScanner'})
MERGE (a3)-[:COMPLEMENTS]->(a23);

// ChartGenerator complements DataAnalyzer
MATCH (a10:Agent {name: 'ChartGenerator'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a10)-[:COMPLEMENTS]->(a9);
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a10:Agent {name: 'ChartGenerator'})
MERGE (a9)-[:COMPLEMENTS]->(a10);

// PredictiveAnalytics complements DataAnalyzer
MATCH (a11:Agent {name: 'PredictiveAnalytics'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a11)-[:COMPLEMENTS]->(a9);
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a11:Agent {name: 'PredictiveAnalytics'})
MERGE (a9)-[:COMPLEMENTS]->(a11);

// DocumentSummarizer complements TextAnalyzer
MATCH (a6:Agent {name: 'DocumentSummarizer'}), (a7:Agent {name: 'TextAnalyzer Pro'})
MERGE (a6)-[:COMPLEMENTS]->(a7);
MATCH (a7:Agent {name: 'TextAnalyzer Pro'}), (a6:Agent {name: 'DocumentSummarizer'})
MERGE (a7)-[:COMPLEMENTS]->(a6);

// ResearchAssistant complements DeepSearch
MATCH (a27:Agent {name: 'ResearchAssistant'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a27)-[:COMPLEMENTS]->(a2);
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a27:Agent {name: 'ResearchAssistant'})
MERGE (a2)-[:COMPLEMENTS]->(a27);

// FactChecker complements WebSearch
MATCH (a28:Agent {name: 'FactChecker'}), (a1:Agent {name: 'WebSearch Pro'})
MERGE (a28)-[:COMPLEMENTS]->(a1);
MATCH (a1:Agent {name: 'WebSearch Pro'}), (a28:Agent {name: 'FactChecker'})
MERGE (a1)-[:COMPLEMENTS]->(a28);

// EmailAssistant complements ChatBot
MATCH (a16:Agent {name: 'EmailAssistant'}), (a15:Agent {name: 'ChatBot Pro'})
MERGE (a16)-[:COMPLEMENTS]->(a15);
MATCH (a15:Agent {name: 'ChatBot Pro'}), (a16:Agent {name: 'EmailAssistant'})
MERGE (a15)-[:COMPLEMENTS]->(a16);

// ----------------------------------------------------------------------------
// PART 5: CREATE WORKS_WITH RELATIONSHIPS
// Agents that are commonly used together in workflows
// ----------------------------------------------------------------------------

// Code analysis workflow
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a4:Agent {name: 'CodeGenerator AI'})
MERGE (a3)-[:WORKS_WITH]->(a4);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a5:Agent {name: 'DebugMaster'})
MERGE (a3)-[:WORKS_WITH]->(a5);
MATCH (a3:Agent {name: 'CodeAnalyzer Pro'}), (a24:Agent {name: 'QualityAssurance'})
MERGE (a3)-[:WORKS_WITH]->(a24);

// Data analysis workflow
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a10:Agent {name: 'ChartGenerator'})
MERGE (a9)-[:WORKS_WITH]->(a10);
MATCH (a9:Agent {name: 'DataAnalyzer Pro'}), (a11:Agent {name: 'PredictiveAnalytics'})
MERGE (a9)-[:WORKS_WITH]->(a11);
MATCH (a10:Agent {name: 'ChartGenerator'}), (a9:Agent {name: 'DataAnalyzer Pro'})
MERGE (a10)-[:WORKS_WITH]->(a9);

// Content creation workflow
MATCH (a12:Agent {name: 'ContentWriter Pro'}), (a14:Agent {name: 'ImageGenerator'})
MERGE (a12)-[:WORKS_WITH]->(a14);
MATCH (a13:Agent {name: 'CreativeAssistant'}), (a14:Agent {name: 'ImageGenerator'})
MERGE (a13)-[:WORKS_WITH]->(a14);

// Research workflow
MATCH (a2:Agent {name: 'DeepSearch Agent'}), (a27:Agent {name: 'ResearchAssistant'})
MERGE (a2)-[:WORKS_WITH]->(a27);
MATCH (a18:Agent {name: 'MedicalResearch'}), (a2:Agent {name: 'DeepSearch Agent'})
MERGE (a18)-[:WORKS_WITH]->(a2);
MATCH (a27:Agent {name: 'ResearchAssistant'}), (a28:Agent {name: 'FactChecker'})
MERGE (a27)-[:WORKS_WITH]->(a28);

// Automation workflow
MATCH (a25:Agent {name: 'WorkflowAutomator'}), (a26:Agent {name: 'APIIntegrator'})
MERGE (a25)-[:WORKS_WITH]->(a26);
MATCH (a26:Agent {name: 'APIIntegrator'}), (a25:Agent {name: 'WorkflowAutomator'})
MERGE (a26)-[:WORKS_WITH]->(a25);

// Media processing workflow
MATCH (a21:Agent {name: 'AudioTranscriber'}), (a22:Agent {name: 'VideoAnalyzer'})
MERGE (a21)-[:WORKS_WITH]->(a22);
MATCH (a22:Agent {name: 'VideoAnalyzer'}), (a6:Agent {name: 'DocumentSummarizer'})
MERGE (a22)-[:WORKS_WITH]->(a6);

// Communication workflow
MATCH (a15:Agent {name: 'ChatBot Pro'}), (a16:Agent {name: 'EmailAssistant'})
MERGE (a15)-[:WORKS_WITH]->(a16);
MATCH (a16:Agent {name: 'EmailAssistant'}), (a8:Agent {name: 'TranslationMaster'})
MERGE (a16)-[:WORKS_WITH]->(a8);

// ============================================================================
// CREATE TASKTYPE NODES AND CONNECT TO CAPABILITIES
// ============================================================================
// This fixes the routing issue where PerplexityFallbackAgent is always selected
// because TaskType nodes were missing from the fresh seed
// ============================================================================

// Create the 5 core TaskType nodes
MERGE (webTask:TaskType {name: 'WebSearchTask', complexityLevel: 0.3});
MERGE (codeTask:TaskType {name: 'CodeDebuggingTask', complexityLevel: 0.8});
MERGE (sumTask:TaskType {name: 'SummarizationTask', complexityLevel: 0.5});
MERGE (vizTask:TaskType {name: 'VisualizationTask', complexityLevel: 0.7});
MERGE (otherTask:TaskType {name: 'OtherTask', complexityLevel: 0.5});

// Connect WebSearchTask to required capabilities
MATCH (webTask:TaskType {name: 'WebSearchTask'}), (webCap:Capability {name: 'WebSearching'})
MERGE (webTask)-[:REQUIRES_CAPABILITY]->(webCap);

MATCH (webTask:TaskType {name: 'WebSearchTask'}), (factCap:Capability {name: 'FactRetrieval'})
MERGE (webTask)-[:REQUIRES_CAPABILITY]->(factCap);

MATCH (webTask:TaskType {name: 'WebSearchTask'}), (researchCap:Capability {name: 'Research'})
MERGE (webTask)-[:REQUIRES_CAPABILITY]->(researchCap);

// Connect CodeDebuggingTask to required capabilities
MATCH (codeTask:TaskType {name: 'CodeDebuggingTask'}), (codeCap:Capability {name: 'CodeUnderstanding'})
MERGE (codeTask)-[:REQUIRES_CAPABILITY]->(codeCap);

MATCH (codeTask:TaskType {name: 'CodeDebuggingTask'}), (debugCap:Capability {name: 'DebuggingAssistance'})
MERGE (codeTask)-[:REQUIRES_CAPABILITY]->(debugCap);

MATCH (codeTask:TaskType {name: 'CodeDebuggingTask'}), (securityCap:Capability {name: 'SecurityScanning'})
MERGE (codeTask)-[:REQUIRES_CAPABILITY]->(securityCap);

MATCH (codeTask:TaskType {name: 'CodeDebuggingTask'}), (codeGenCap:Capability {name: 'CodeGeneration'})
MERGE (codeTask)-[:REQUIRES_CAPABILITY]->(codeGenCap);

// Connect SummarizationTask to required capabilities
MATCH (sumTask:TaskType {name: 'SummarizationTask'}), (sumCap:Capability {name: 'DocumentSummarization'})
MERGE (sumTask)-[:REQUIRES_CAPABILITY]->(sumCap);

MATCH (sumTask:TaskType {name: 'SummarizationTask'}), (textCap:Capability {name: 'TextAnalysis'})
MERGE (sumTask)-[:REQUIRES_CAPABILITY]->(textCap);

// Connect VisualizationTask to required capabilities
MATCH (vizTask:TaskType {name: 'VisualizationTask'}), (vizCap:Capability {name: 'DataVisualization'})
MERGE (vizTask)-[:REQUIRES_CAPABILITY]->(vizCap);

MATCH (vizTask:TaskType {name: 'VisualizationTask'}), (dataCap:Capability {name: 'DataAnalysis'})
MERGE (vizTask)-[:REQUIRES_CAPABILITY]->(dataCap);

// Connect OtherTask to general capability (fallback for ambiguous queries)
MATCH (otherTask:TaskType {name: 'OtherTask'}), (genCap:Capability {name: 'GeneralKnowledge'})
MERGE (otherTask)-[:REQUIRES_CAPABILITY]->(genCap);

MATCH (otherTask:TaskType {name: 'OtherTask'}), (convCap:Capability {name: 'ConversationalAI'})
MERGE (otherTask)-[:REQUIRES_CAPABILITY]->(convCap);

