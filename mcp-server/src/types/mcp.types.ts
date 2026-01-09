import type { JsonRpcRequestTransport, JsonRpcResponseTransport } from './json-rpc.types'
import type { JsonObj } from './server.types'
import type { ClientCapabilities, McpClientServerInfo, McpToolCallResultContent, McpToolsResult, ServerCapabilities } from './feature.types'
import type { McpResourceLink } from './mcp-resource.types'

/**
 * Complete MCP Method Enum
 * @see https://spec.modelcontextprotocol.io/specification/basic/
 */
export enum McpMethodEnum {
  // Lifecycle
  INITIALIZE = 'initialize',
  NOTIFICATIONS_INITIALIZED = 'notifications/initialized',

  // Tools
  TOOLS_LIST = 'tools/list',
  TOOLS_CALL = 'tools/call',

  // Resources
  RESOURCES_LIST = 'resources/list',
  RESOURCES_READ = 'resources/read',
  RESOURCES_SUBSCRIBE = 'resources/subscribe',
  RESOURCES_UNSUBSCRIBE = 'resources/unsubscribe',

  // Prompts
  PROMPTS_LIST = 'prompts/list',
  PROMPTS_GET = 'prompts/get',

  // Logging
  LOGGING_SET_LEVEL = 'logging/setLevel',

  // Sampling
  SAMPLING_CREATE_MESSAGE = 'sampling/createMessage',

  // Completion
  COMPLETION_COMPLETE = 'completion/complete',

  // Notifications
  NOTIFICATIONS_MESSAGE = 'notifications/message',
  NOTIFICATIONS_RESOURCES_LIST_CHANGED = 'notifications/resources/list_changed',
  NOTIFICATIONS_TOOLS_LIST_CHANGED = 'notifications/tools/list_changed',
  NOTIFICATIONS_PROMPTS_LIST_CHANGED = 'notifications/prompts/list_changed',
}

///////////////////////////////////
/// Incoming request parameters ///
///////////////////////////////////
export interface McpRequestParams {
  protocolVersion: '2024-11-05' | '2025-11-25' // Changed from '2025-11-25' to supported version
  capabilities: ClientCapabilities
  clientInfo: McpClientServerInfo
}

export interface McpToolCallParams {
  name: string
  arguments: JsonObj
}
////////////////////////////////
/// Outgoing response result ///
////////////////////////////////
export interface McpCapabilitiesResult {
  protocolVersion?: '2024-11-05' | '2025-11-25' // Changed from '2025-11-25' to supported version
  capabilities: ServerCapabilities
  serverInfo: McpClientServerInfo
}

export interface McpToolCallResult {
  content: McpToolCallResultContent[]
  isError?: boolean
  _meta?: JsonObj
}

export interface McpResourceListResult {
  resources: McpResourceLink[]
}

//////////////////////////////
/// Incoming request types ///
//////////////////////////////
export interface McpRequestTransport<T = JsonObj | null | undefined> extends JsonRpcRequestTransport<T> {
  method: McpMethodEnum | string
}

export interface InitializeMCPServerRequest extends McpRequestTransport<McpRequestParams> {
  method: McpMethodEnum.INITIALIZE
}

export interface ToolListMCPServerRequest extends McpRequestTransport {
  method: McpMethodEnum.TOOLS_LIST
}

export interface ToolCallMCPServerRequest extends McpRequestTransport<McpToolCallParams> {
  method: McpMethodEnum.TOOLS_CALL
}

///////////////////////////////
/// Outgoing Response types ///
///////////////////////////////
export type McpResponseTransport = JsonRpcResponseTransport

export interface McpInitializeMCPServerResponse extends McpResponseTransport {
  result: McpCapabilitiesResult
}

export interface McpToolListResponse extends McpResponseTransport {
  result: McpToolsResult
}

export interface McpToolCallResponse extends McpResponseTransport {
  result: McpToolCallResult
}
