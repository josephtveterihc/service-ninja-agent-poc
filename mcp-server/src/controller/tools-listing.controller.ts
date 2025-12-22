import { environmentToolSchemas } from '../tool-schema/environment.schema'
import { projectToolSchemas } from '../tool-schema/project.schema'
import { resourceToolSchemas } from '../tool-schema/resource.schema'
import { resourceMonitoringToolSchemas } from '../tool-schema/resource-monitoring.schema'
import type { McpToolsResponse } from '../types'

export function ToolsListingController(): McpToolsResponse {
  console.log('--- ToolsListingController ---')
  return {
    tools: [...projectToolSchemas, ...environmentToolSchemas, ...resourceToolSchemas, ...resourceMonitoringToolSchemas],
  }
}
