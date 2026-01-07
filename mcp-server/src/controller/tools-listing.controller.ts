import type { McpToolsResult } from '../types'
import { toolSchemaList } from '../tool-schema'

export function ToolsListingController(): McpToolsResult {
  console.log('--- ToolsListingController ---')
  return {
    tools: toolSchemaList,
  }
}
