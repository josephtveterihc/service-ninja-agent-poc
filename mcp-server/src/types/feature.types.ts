import type { JsonObj } from './server.types'

export interface McpPropertySchema {
  type: 'string' | 'number' | 'boolean' | 'array' | 'object'
  description?: string
  default?: string | number | boolean | JsonObj
  minLength?: number
  maxLength?: number
  minimum?: number
  maximum?: number
  format?: string
}
export interface McpInputSchema {
  type: 'object'
  properties: Record<string, McpPropertySchema>
  required?: string[]
}
export interface McpToolSchema {
  name: string
  description: string
  inputSchema: McpInputSchema
  functionName?: string // TODO - Remove later
}

export interface McpToolsResult {
  tools: McpToolSchema[]
}

export interface McpToolCallResultContent {
  type: 'text' | 'image' | 'resource' | 'audio' | 'video' | 'file'
  text: string
  data?: string
  mimeType?: string
}

/**
 * Client Capabilities Structure
 * Describes the capabilities supported by the MCP client.
 * @see https://modelcontextprotocol.io/specification/2025-11-25/schema#clientcapabilities
 */
export interface ClientCapabilities {
  /**
   * Present if the client supports sampling
   */
  sampling?: {
    context?: JsonObj
    tools?: JsonObj
  }

  /**
   * Present if the client supports elicitation
   */
  elicitation?: {
    form?: JsonObj
    url?: JsonObj
  }

  /**
   * Present if the client supports receiving notifications for roots list changes
   */
  roots?: {
    /**
     * Whether the client supports being notified when the roots list changes
     */
    listChanged?: boolean
  }

  tasks?: {
    list?: JsonObj
    cancel?: JsonObj
    requests?: {
      sampling?: {
        createMessage?: JsonObj
      }
      elecitation?: {
        create?: JsonObj
      }
    }
  }

  /**
   * Present if the client supports experimental features
   */
  experimental?: JsonObj
}

/**
 * Server Capabilities Structure
 * Describes the capabilities supported by the MCP server.
 * @see https://modelcontextprotocol.io/specification/2025-11-25/schema#servercapabilities
 */
export interface ServerCapabilities {
  experimental?: JsonObj
  logging?:
    | boolean
    | {
        level: 'debug' | 'info' | 'notice' | 'warning' | 'error' | 'critical' | 'alert' | 'emergency'
      }
  completions?: JsonObj
  prompts?: { listChanged?: boolean }
  resources?: { subscribe?: boolean; listChanged?: boolean }
  tools?: { listChanged?: boolean }
  tasks?: {
    list?: JsonObj
    cancel?: JsonObj
    requests?: { tools?: { call?: JsonObj } }
  }
}

export interface McpClientServerInfo {
  name: string
  version: string
}
