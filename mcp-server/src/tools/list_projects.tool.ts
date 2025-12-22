import { type McpToolCallResponse } from '../types/server.types.js'

interface ListProjectsArgs {
  environment?: string
  status?: string
  limit?: number
  includeStats?: boolean
}

export function listProjectsTool(args: Record<string, any>): McpToolCallResponse {
  try {
    const { 
      environment, 
      status, 
      limit = 20, 
      includeStats = false 
    } = args as ListProjectsArgs

    const sanitizedLimit = typeof limit === 'number' && limit > 0 && limit <= 100 ? limit : 20

    // Mock projects data
    const allProjects = [
      {
        projectId: 'proj_001',
        projectName: 'E-Commerce Platform',
        environment: 'prod',
        status: 'healthy',
        serviceCount: 8,
        lastUpdated: '2024-12-18T08:30:00Z',
        uptime: '99.97%',
        stats: includeStats ? {
          totalRequests: 1250000,
          avgResponseTime: 145,
          errorRate: 0.002,
          activeAlerts: 0
        } : undefined
      },
      {
        projectId: 'proj_002',
        projectName: 'User Management System',
        environment: 'prod',
        status: 'healthy',
        serviceCount: 4,
        lastUpdated: '2024-12-18T07:45:00Z',
        uptime: '99.95%',
        stats: includeStats ? {
          totalRequests: 890000,
          avgResponseTime: 98,
          errorRate: 0.001,
          activeAlerts: 0
        } : undefined
      },
      {
        projectId: 'proj_003',
        projectName: 'Analytics Dashboard',
        environment: 'staging',
        status: 'degraded',
        serviceCount: 6,
        lastUpdated: '2024-12-18T09:15:00Z',
        uptime: '98.82%',
        stats: includeStats ? {
          totalRequests: 567000,
          avgResponseTime: 234,
          errorRate: 0.015,
          activeAlerts: 2
        } : undefined
      },
      {
        projectId: 'proj_004',
        projectName: 'Mobile API Gateway',
        environment: 'dev',
        status: 'healthy',
        serviceCount: 3,
        lastUpdated: '2024-12-18T06:20:00Z',
        uptime: '97.45%',
        stats: includeStats ? {
          totalRequests: 123000,
          avgResponseTime: 189,
          errorRate: 0.008,
          activeAlerts: 1
        } : undefined
      },
      {
        projectId: 'proj_005',
        projectName: 'Payment Processing',
        environment: 'prod',
        status: 'healthy',
        serviceCount: 5,
        lastUpdated: '2024-12-18T08:00:00Z',
        uptime: '99.99%',
        stats: includeStats ? {
          totalRequests: 2100000,
          avgResponseTime: 67,
          errorRate: 0.0005,
          activeAlerts: 0
        } : undefined
      }
    ]

    // Apply filters
    let filteredProjects = allProjects

    if (environment) {
      filteredProjects = filteredProjects.filter(p => p.environment === environment)
    }

    if (status) {
      filteredProjects = filteredProjects.filter(p => p.status === status)
    }

    // Apply limit
    const projects = filteredProjects.slice(0, sanitizedLimit)

    const result = {
      projects,
      totalFound: filteredProjects.length,
      limit: sanitizedLimit,
      filters: {
        environment: environment || 'all',
        status: status || 'all'
      },
      includeStats,
      retrievedAt: new Date().toISOString()
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }],
      _meta: {
        toolName: 'list_projects',
        executionTime: Date.now()
      }
    }
  } catch (error) {
    return {
      isError: true,
      content: [{
        type: 'text',
        text: `Failed to list projects: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]
    }
  }
}