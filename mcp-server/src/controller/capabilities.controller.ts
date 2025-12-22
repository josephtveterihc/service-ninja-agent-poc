import packageJson from '../../package.json'
import type { McpCapabilitiesResponse } from '../types'

export function CapabilitiesController(): McpCapabilitiesResponse {
  return {
    capabilities: {
      resources: false,
      tools: {
        listChanged: false,
        subscribe: false,
      },
      prompts: false,
      logging: false,
    },
    serverInfo: {
      name: packageJson.name || 'service-ninja-mcp-server',
      version: packageJson.version || '1.0.0',
    },
  }
}
