import packageJson from '../../package.json'
import type { McpCapabilitiesResult } from '../types'

export function CapabilitiesController(): McpCapabilitiesResult {
  return {
    protocolVersion: '2025-11-25',
    capabilities: {
      // resources: false,
      tools: {
        listChanged: true,
        // subscribe: false,
      },
      // prompts: false,
      // logging: false,
    },
    serverInfo: {
      name: packageJson.name || 'service-ninja-mcp-server',
      version: packageJson.version || '1.0.0',
    },
  }
}
