import axios from 'axios'
import { getServiceNinjaResource, getServiceNinjaResources } from '../repo/service-ninja-repo'
import type { ServiceNinjaResource } from '../sql-lite/sql-lite-table.types'
import type { McpToolCallResult } from '../types'

export async function getResourceHealthStatusTool({ resourceId }: { resourceId: number }): Promise<McpToolCallResult> {
  console.log('--- getResourceHealthStatusTool ---')
  try {
    const resource = (await getServiceNinjaResource({ id: resourceId })) as ServiceNinjaResource
    if (!resource) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Resource with ID ${resourceId} not found`,
          },
        ],
      }
    }

    const { name, headers, healthCheckUrl } = resource
    if (!healthCheckUrl) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No health check URL configured for resource "${name}"`,
          },
        ],
      }
    }

    const res = await axios.get(healthCheckUrl || '', { headers: headers ? JSON.parse(headers) : {} })
    console.log(`--- Health check response for resource "${name}":`, res.data)

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(res.data),
        },
      ],
    }
  } catch (err) {
    const error = err as Error
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to get resource health status: ${error.message}`,
        },
      ],
    }
  }
}

export async function getProjectResourcesHealthStatusTool({ projectId, envId }: { projectId: number; envId: number }): Promise<McpToolCallResult> {
  console.log('--- getProjectResourcesHealthStatusTool ---')
  try {
    const resources = (await getServiceNinjaResources(projectId, envId)) as ServiceNinjaResource[]

    if (!resources || resources.length === 0) {
      return {
        isError: false,
        content: [
          {
            type: 'text',
            text: JSON.stringify([]),
          },
        ],
      }
    }

    const healthResults = []
    for (const resource of resources) {
      if (resource.healthCheckUrl) {
        try {
          const headers = resource.headers ? JSON.parse(resource.headers) : {}
          const res = await axios.get(resource.healthCheckUrl, { headers })
          healthResults.push({
            resourceId: resource.id,
            resourceName: resource.name,
            status: 'healthy',
            data: res.data,
          })
        } catch (error) {
          healthResults.push({
            resourceId: resource.id,
            resourceName: resource.name,
            status: 'unhealthy',
            error: error instanceof Error ? error.message : 'Unknown error',
          })
        }
      } else {
        healthResults.push({
          resourceId: resource.id,
          resourceName: resource.name,
          status: 'no_health_check',
          message: 'No health check URL configured',
        })
      }
    }

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify(healthResults),
        },
      ],
    }
  } catch (err) {
    const error = err as Error
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Failed to get project resources health status: ${error.message}`,
        },
      ],
    }
  }
}

export async function getResourceAliveStatusTool({ resourceId }: { resourceId: number }): Promise<McpToolCallResult> {
  console.log('--- getResourceAliveStatusTool ---')
  try {
    if (!resourceId) {
      console.warn('--- Resource ID not provided ---')
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Resource ID is required',
          },
        ],
      }
    }
    const resource = (await getServiceNinjaResource({ id: resourceId })) as ServiceNinjaResource
    if (!resource) {
      console.warn(`--- Resource with ID ${resourceId} not found ---`)
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Resource with ID ${resourceId} not found`,
          },
        ],
      }
    }

    const { name, headers, aliveCheckUrl } = resource
    if (!aliveCheckUrl) {
      console.warn(`--- No alive check URL configured for resource "${name}" ---`)
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `No alive check URL configured for resource "${name}"`,
          },
        ],
      }
    }

    const res = await axios.get(aliveCheckUrl, {
      headers: headers ? JSON.parse(headers) : {},
      timeout: 5000, // 5 second timeout for alive checks
    })

    console.log(`--- Alive check response for resource "${name}":`, res.status)

    return {
      isError: false,
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            alive: true,
            statusCode: res.status,
            responseTime: Date.now(),
          }),
        },
      ],
    }
  } catch (err) {
    const error = err as Error
    return {
      isError: false, // Not an error - resource is just not alive
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            alive: false,
            error: error.message,
          }),
        },
      ],
    }
  }
}
