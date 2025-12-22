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

// export interface ServerInfo {
//   name: string
//   version: string
//   capabilities: ServerCapabilities
// }

export interface ErrorResponse {
  code: number
  message: string
  data?: any
}

export interface SuccessResponse<T = any> {
  result: T
}

export type ServerResponse<T = any> = SuccessResponse<T> | ErrorResponse

export type McpCapabilityStatus = boolean | { subscribe?: boolean; listChanged?: boolean }

export interface McpCapabilities {
  resources?: McpCapabilityStatus
  tools?: McpCapabilityStatus
  prompts?: McpCapabilityStatus
  logging?:
    | boolean
    | {
        level: 'debug' | 'info' | 'notice' | 'warning' | 'error' | 'critical' | 'alert' | 'emergency'
      }
}

export interface McpServerInfo {
  name: string
  version: string
}

export interface McpCapabilitiesResponse {
  capabilities: McpCapabilities
  serverInfo: McpServerInfo
}

export interface McpToolCallRequest {
  name: string
  arguments: Record<string, any>
}

export interface McpToolCallContent {
  type: 'text' | 'image' | 'resource'
  text: string
  data?: string
  mimeType?: string
}

export interface McpToolCallResponse {
  content: McpToolCallContent[]
  isError?: boolean
  _meta?: Record<string, any>
}
