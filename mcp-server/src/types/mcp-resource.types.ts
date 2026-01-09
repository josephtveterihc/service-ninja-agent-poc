import type { JsonObj } from '../types'

export interface McpResourceIcon {
  src: string
  mimeType?: string
  sizes?: string[]
  theme?: 'light' | 'dark'
}
export type McpResourceRole = 'user' | 'assistant'
export interface McpResourceAnnotations {
  audience?: McpResourceRole[]
  priority?: number
  lastModified?: string
}

export interface McpResourceLink {
  icons?: McpResourceIcon[]
  name: string
  title?: string
  uri: string
  description?: string
  mimeType?: string
  annotations?: McpResourceAnnotations
  size?: number
  _meta?: JsonObj
  type: 'resource_link'
}
