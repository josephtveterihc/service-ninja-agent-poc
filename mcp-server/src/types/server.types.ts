export type JsonObj = Record<string, any>
export interface AliveCheckResponse {
  serviceName?: string
  alive: boolean
  timestamp: string
  statusCode?: number
  info: {
    version: string
    branch: string
    author: string
  }
}

export enum HealthStatus {
  UP = 'up',
  DOWN = 'down',
}
export interface HealthCheckResponse extends AliveCheckResponse {
  dependencies: {
    required: Record<string, HealthStatus>
    optional: Record<string, HealthStatus>
  }
  health: HealthStatus
}

export interface ServerConfig {
  port: number
  host: string
  name: string
  version: string
}
