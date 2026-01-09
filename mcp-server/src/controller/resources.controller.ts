import type { McpResourceListResult } from '../types'
import { resourceList } from '../resource-schema'

export function ResourcesController(params: { cursor?: string }): McpResourceListResult {
  return {
    resources: resourceList,
  }
}
