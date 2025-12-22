import type { McpToolSchema } from '../types'

export const resourceMonitoringToolSchemas: McpToolSchema[] = [
  {
    name: 'get_resource_health_status',
    description: 'Get health status of a specific resource by making a request to its health check URL',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'The ID of the resource to check health status for',
        },
      },
      required: ['resourceId'],
    },
  },
  {
    name: 'get_project_resources_health_status',
    description: 'Get health status of all resources in a specific project environment',
    inputSchema: {
      type: 'object',
      properties: {
        projectId: {
          type: 'number',
          description: 'The ID of the project containing the resources',
        },
        envId: {
          type: 'number',
          description: 'The ID of the environment within the project',
        },
      },
      required: ['projectId', 'envId'],
    },
  },
  {
    name: 'get_resource_alive_status',
    description: 'Check if a specific resource is alive and responding by making a request to its alive check URL',
    inputSchema: {
      type: 'object',
      properties: {
        resourceId: {
          type: 'number',
          description: 'The ID of the resource to check alive status for',
        },
      },
      required: ['resourceId'],
    },
  },
]
