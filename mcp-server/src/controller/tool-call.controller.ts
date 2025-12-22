import {
  createServiceNinjaProjectTool,
  deleteServiceNinjaProjectTool,
  getProjectToolListTool,
  readServiceNinjaProjectTool,
  updateServiceNinjaProjectTool,
} from '../tools/service-ninja/service-ninja-project.tool.js'
import {
  createServiceNinjaEnvironmentTool,
  deleteServiceNinjaEnvironmentTool,
  getEnvironmentToolListTool,
  readServiceNinjaEnvironmentTool,
  updateServiceNinjaEnvironmentTool,
} from '../tools/service-ninja/service-ninja-environment.tool.js'
import {
  createServiceNinjaResourceTool,
  deleteServiceNinjaResourceTool,
  getResourceToolListTool,
  readServiceNinjaResourceTool,
  updateServiceNinjaResourceTool,
} from '../tools/service-ninja/service-ninja-resource.tool.js'
import { type McpToolCallRequest, type McpToolCallResponse } from '../types/server.types.js'
import type { ServiceNinjaEnv, ServiceNinjaResource } from '../sql-lite/sql-lite-table.types.js'
import { getProjectResourcesHealthStatusTool, getResourceAliveStatusTool, getResourceHealthStatusTool } from '../tools/resource_monitor.tool.js'

export async function ToolCallController({ body }: { body: McpToolCallRequest }): Promise<McpToolCallResponse> {
  console.log('--- ToolCallController ---')
  try {
    if (!body || typeof body !== 'object') {
      console.warn('--- Invalid request body ---', body)
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Invalid request body',
          },
        ],
      }
    }

    const { name, arguments: args } = body
    console.log('name:', name)

    if (!name || typeof name !== 'string') {
      console.warn('--- Missing or invalid tool name ---', name)
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: 'Missing or invalid tool name',
          },
        ],
      }
    }

    // Route to appropriate tool
    switch (name) {
      // Project tools
      case 'create_project':
        return createServiceNinjaProjectTool(args as { name: string; description: string })
      case 'list_projects':
        return getProjectToolListTool()
      case 'get_project_by_id':
      case 'get_project_by_name':
        return readServiceNinjaProjectTool(args as { name?: string; id?: number })
      case 'update_project':
        return updateServiceNinjaProjectTool(args as { id: number; name?: string; description?: string })
      case 'delete_project':
        return deleteServiceNinjaProjectTool(args as { id: number })

      // Environment tools
      case 'create_environment':
        return createServiceNinjaEnvironmentTool(args as Partial<ServiceNinjaEnv>)
      case 'list_environments':
        return getEnvironmentToolListTool((args as { projectId?: number })?.projectId)
      case 'get_environment_by_id':
      case 'get_environment_by_name':
        return readServiceNinjaEnvironmentTool(args as { name?: string; id?: number; projectId?: number })
      case 'update_environment':
        return updateServiceNinjaEnvironmentTool(args as Partial<ServiceNinjaEnv> & { id: number })
      case 'delete_environment':
        return deleteServiceNinjaEnvironmentTool(args as { id: number })

      // Resource tools
      case 'create_resource':
        return createServiceNinjaResourceTool(args as Partial<ServiceNinjaResource>)
      case 'list_resources':
        return getResourceToolListTool((args as { projectId?: number; envId?: number })?.projectId, (args as { projectId?: number; envId?: number })?.envId)
      case 'get_resource_by_id':
      case 'get_resource_by_name':
        return readServiceNinjaResourceTool(args as { name?: string; id?: number; projectId?: number; envId?: number })
      case 'update_resource':
        return updateServiceNinjaResourceTool(args as Partial<ServiceNinjaResource> & { id: number })
      case 'delete_resource':
        return deleteServiceNinjaResourceTool(args as { id: number })

      // Resource Monitoring tools
      case 'get_resource_health_status':
        return getResourceHealthStatusTool(args as { resourceId: number })
      case 'get_project_resources_health_status':
        return getProjectResourcesHealthStatusTool(args as { projectId: number; envId: number })
      case 'get_resource_alive_status':
        return getResourceAliveStatusTool(args as { resourceId: number })

      default:
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `Unknown tool: ${name}`,
            },
          ],
        }
    }
  } catch (error) {
    console.error('--- ToolCallController error ---', error)
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Tool execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`,
        },
      ],
    }
  }
}
