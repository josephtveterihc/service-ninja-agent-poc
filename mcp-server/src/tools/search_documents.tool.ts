import { type McpToolCallResponse } from '../types/server.types.js'

interface SearchDocumentsArgs {
  query: string
  limit?: number
  category?: string
  includeContent?: boolean
}

export function searchDocumentsTool(args: Record<string, any>): McpToolCallResponse {
  try {
    const { query, limit = 10, category, includeContent = false } = args as SearchDocumentsArgs

    // Input validation
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'query is required and must be a non-empty string'
        }]
      }
    }

    const sanitizedLimit = typeof limit === 'number' && limit > 0 && limit <= 100 ? limit : 10
    const sanitizedQuery = query.trim().toLowerCase()

    // Mock document search with realistic results
    const mockDocuments = [
      {
        id: 'doc_001',
        title: 'Service Monitoring Best Practices',
        excerpt: 'Comprehensive guide to monitoring microservices in production environments',
        category: 'monitoring',
        lastModified: '2024-12-15T10:30:00Z',
        relevance: 0.95,
        content: includeContent ? 'Full content of monitoring best practices document...' : undefined
      },
      {
        id: 'doc_002',
        title: 'Project Setup Guidelines',
        excerpt: 'Step-by-step instructions for setting up new monitoring projects',
        category: 'setup',
        lastModified: '2024-12-14T14:22:00Z',
        relevance: 0.87,
        content: includeContent ? 'Full content of project setup guidelines...' : undefined
      },
      {
        id: 'doc_003',
        title: 'Alert Configuration Reference',
        excerpt: 'Complete reference for configuring monitoring alerts and notifications',
        category: 'alerts',
        lastModified: '2024-12-13T09:15:00Z',
        relevance: 0.82,
        content: includeContent ? 'Full content of alert configuration reference...' : undefined
      },
      {
        id: 'doc_004',
        title: 'Health Check Implementation Guide',
        excerpt: 'How to implement effective health checks for your services',
        category: 'health-checks',
        lastModified: '2024-12-12T16:45:00Z',
        relevance: 0.78,
        content: includeContent ? 'Full content of health check implementation guide...' : undefined
      }
    ]

    // Filter by category if provided
    let filteredDocs = category 
      ? mockDocuments.filter(doc => doc.category === category)
      : mockDocuments

    // Simple text matching (in a real implementation, this would use proper search)
    filteredDocs = filteredDocs.filter(doc => 
      doc.title.toLowerCase().includes(sanitizedQuery) ||
      doc.excerpt.toLowerCase().includes(sanitizedQuery) ||
      doc.category.toLowerCase().includes(sanitizedQuery)
    )

    // Sort by relevance and apply limit
    const results = filteredDocs
      .sort((a, b) => b.relevance - a.relevance)
      .slice(0, sanitizedLimit)

    const searchResult = {
      query: sanitizedQuery,
      results,
      totalFound: results.length,
      limit: sanitizedLimit,
      category: category || 'all',
      includeContent,
      searchedAt: new Date().toISOString()
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(searchResult, null, 2)
      }],
      _meta: {
        toolName: 'search_documents',
        executionTime: Date.now()
      }
    }
  } catch (error) {
    return {
      isError: true,
      content: [{
        type: 'text',
        text: `Failed to search documents: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]
    }
  }
}