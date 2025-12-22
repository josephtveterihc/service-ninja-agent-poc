import packageJson from '../../package.json'
import { HealthStatus, type HealthCheckResponse } from '../types/server.types'
import branchName from 'current-git-branch'

export function HealthCheckController(): HealthCheckResponse {
  console.log('--- HealthCheckController ---')
  return {
    serviceName: packageJson.name || 'service-ninja-mcp-server',
    statusCode: 200,
    alive: true,
    timestamp: new Date().toISOString(),
    dependencies: {
      required: {},
      optional: {},
    },
    health: HealthStatus.UP,
    info: {
      version: packageJson.version,
      branch: branchName() || 'unknown',
      author: packageJson.author,
    },
  }
}
