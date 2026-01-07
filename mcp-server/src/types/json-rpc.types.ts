import type { JsonObj } from './server.types'

/**
 * JSON-RPC 2.0 Transport Structure
 * @see https://www.jsonrpc.org/specification
 */

export interface JsonRpcTransport {
  jsonrpc: '2.0' // A String specifying the version of the JSON-RPC protocol. MUST be exactly "2.0".
  id: string | number // An identifier established by the Client that MUST contain a String, Number, or NULL value if included. If it is not included it is assumed to be a notification. The value SHOULD normally not be Null and Numbers SHOULD NOT contain fractional parts
}

export interface JsonRpcRequestTransport<T = JsonObj | null | undefined> extends JsonRpcTransport {
  method: string // A String containing the name of the method to be invoked. Method names that begin with the word rpc followed by a period character (U+002E or ASCII 46) are reserved for rpc-internal methods and extensions and MUST NOT be used for anything else.
  params?: T // A Structured value that holds the parameter values to be used during the invocation of the method. This member MAY be omitted.
}

export interface JsonRpcError {
  code: number // A Number that indicates the error type that occurred. This MUST be an integer.
  message: string // A String providing a short description of the error. The message SHOULD be limited to a concise single sentence.
  data?: JsonObj // A Primitive or Structured value that contains additional information about the error. This may be omitted.
}

export interface JsonRpcResponseTransport<T = JsonObj | null | undefined> extends JsonRpcTransport {
  // id: string | number | null // This member is REQUIRED. It MUST be the same as the value of the id member in the Request Object.
  result?: T // This member is REQUIRED on success. This member MUST NOT exist if there was an error invoking the method. The value of this member is determined by the method invoked on the Server.
  error?: JsonRpcError // This member is REQUIRED on error. This member MUST NOT exist if there was no error triggered during invocation. The value for this member MUST be an Object as defined in section 5.1.
}
