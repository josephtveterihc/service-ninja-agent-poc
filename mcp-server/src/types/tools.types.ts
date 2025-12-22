export interface McpPropertySchema {
  type: 'string' | 'number' | 'boolean' | 'array' | 'object'
  description?: string
  default?: any
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
}

export interface McpToolsResponse {
  tools: McpToolSchema[]
}
