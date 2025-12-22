import type { AliveCheckResponse } from '../types'
import packageJson from '../../package.json'
import branchName from 'current-git-branch'

export function AliveController(): AliveCheckResponse {
  return {
    serviceName: packageJson.name || 'service-ninja-mcp-server',
    statusCode: 200,
    alive: true,
    timestamp: new Date().toISOString(),
    info: {
      version: packageJson.version,
      branch: branchName() || 'unknown',
      author: packageJson.author,
    },
  }
}
