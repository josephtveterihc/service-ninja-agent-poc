import { type McpToolCallResponse } from '../types/server.types.js'

interface GetProjectStatusArgs {
  projectId: string
  includeServices?: boolean
  includeAlerts?: boolean
}

export function getProjectStatusTool(args: Record<string, any>): McpToolCallResponse {
  try {
    const { projectId, includeServices = true, includeAlerts = false } = args as GetProjectStatusArgs

    // Input validation
    if (!projectId || typeof projectId !== 'string' || projectId.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'projectId is required and must be a non-empty string'
        }]
      }
    }

    // Mock project status data
    const projectStatus = {
      projectId: projectId.trim(),
      projectName: `Project ${projectId}`,
      environment: 'prod',
      status: 'healthy',
      lastChecked: new Date().toISOString(),
      uptime: '99.95%',
      totalServices: 5,
      healthyServices: 5,
      unhealthyServices: 0,
      services: includeServices ? [
        {
          serviceId: 'svc_001',
          serviceName: 'user-api',
          status: 'healthy',
          lastCheck: new Date(Date.now() - 30000).toISOString(),
          responseTime: 125,
          healthCheckUrl: 'https://api.example.com/health'
        },
        {
          serviceId: 'svc_002',
          serviceName: 'auth-service',
          status: 'healthy',
          lastCheck: new Date(Date.now() - 45000).toISOString(),
          responseTime: 89,
          healthCheckUrl: 'https://auth.example.com/health'
        },
        {
          serviceId: 'svc_003',
          serviceName: 'notification-service',
          status: 'healthy',
          lastCheck: new Date(Date.now() - 15000).toISOString(),
          responseTime: 201,
          healthCheckUrl: 'https://notifications.example.com/health'
        }
      ] : undefined,
      alerts: includeAlerts ? [
        {
          alertId: 'alert_001',
          level: 'info',
          message: 'All services operating normally',
          timestamp: new Date(Date.now() - 600000).toISOString(),
          resolved: true
        }
      ] : undefined,
      metrics: {
        avgResponseTime: 138,
        errorRate: 0.001,
        requestsPerMinute: 1247
      }
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(projectStatus, null, 2)
      }],
      _meta: {
        toolName: 'get_project_status',
        executionTime: Date.now()
      }
    }
  } catch (error) {
    return {
      isError: true,
      content: [{
        type: 'text',
        text: `Failed to get project status: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]
    }
  }
}