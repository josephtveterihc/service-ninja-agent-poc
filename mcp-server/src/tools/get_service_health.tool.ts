import { type McpToolCallResponse } from '../types/server.types.js'

interface GetServiceHealthArgs {
  serviceId: string
  includeMetrics?: boolean
  includeHistory?: boolean
}

export function getServiceHealthTool(args: Record<string, any>): McpToolCallResponse {
  try {
    const { serviceId, includeMetrics = true, includeHistory = false } = args as GetServiceHealthArgs

    // Input validation
    if (!serviceId || typeof serviceId !== 'string' || serviceId.trim().length === 0) {
      return {
        isError: true,
        content: [{
          type: 'text',
          text: 'serviceId is required and must be a non-empty string'
        }]
      }
    }

    // Mock service health data
    const serviceHealth = {
      serviceId: serviceId.trim(),
      serviceName: `Service ${serviceId}`,
      status: 'healthy',
      lastChecked: new Date().toISOString(),
      healthCheckUrl: 'https://api.example.com/health',
      responseTime: 142,
      uptime: '99.98%',
      version: '1.2.3',
      environment: 'prod',
      metrics: includeMetrics ? {
        cpu: 45.2,
        memory: 67.8,
        diskUsage: 23.1,
        networkIn: 1024.5,
        networkOut: 856.7,
        activeConnections: 127,
        requestsPerSecond: 20.8,
        errorRate: 0.002
      } : undefined,
      history: includeHistory ? [
        {
          timestamp: new Date(Date.now() - 300000).toISOString(),
          status: 'healthy',
          responseTime: 138
        },
        {
          timestamp: new Date(Date.now() - 600000).toISOString(),
          status: 'healthy', 
          responseTime: 145
        },
        {
          timestamp: new Date(Date.now() - 900000).toISOString(),
          status: 'healthy',
          responseTime: 132
        }
      ] : undefined,
      dependencies: [
        {
          name: 'database',
          status: 'healthy',
          lastCheck: new Date(Date.now() - 60000).toISOString()
        },
        {
          name: 'cache',
          status: 'healthy',
          lastCheck: new Date(Date.now() - 45000).toISOString()
        }
      ]
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(serviceHealth, null, 2)
      }],
      _meta: {
        toolName: 'get_service_health',
        executionTime: Date.now()
      }
    }
  } catch (error) {
    return {
      isError: true,
      content: [{
        type: 'text',
        text: `Failed to get service health: ${error instanceof Error ? error.message : 'Unknown error'}`
      }]
    }
  }
}