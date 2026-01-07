import { Elysia, sse } from 'elysia'
import * as DotEnv from 'dotenv'
import express from 'express'
import expressCors from 'cors'
import { cors } from '@elysiajs/cors'
import { HealthCheckController } from './src/controller/health-check.controller'
import { AliveController } from './src/controller/alive.controller'
import { CapabilitiesController } from './src/controller/capabilities.controller'
import { ToolsListingController } from './src/controller/tools-listing.controller'
import { ToolCallController } from './src/controller/tool-call.controller'
import { getOrCreateSqlLite } from './src/sql-lite/sql-lite.init'
import type { McpResponseTransport, McpInitializeMCPServerResponse, McpToolCallResponse, McpToolListResponse, McpRequestTransport } from './src/types'

import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js'
import { mcpServer } from './src/mcp/server'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'

DotEnv.config()

const server_port = process.env.SERVER_PORT || 3000
let reqNum = 0
/*
HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: mcp-session-id
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
mcp-session-id: a98972b4-e59b-44fe-b8c5-4c1021959ab5
Date: Tue, 06 Jan 2026 22:36:33 GMT
Transfer-Encoding: chunked



HTTP/1.1 200 OK
X-Powered-By: Express
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: mcp-session-id
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
mcp-session-id: 522c9d45-d848-4955-aff1-b941bc7cd9b6
Date: Tue, 06 Jan 2026 23:05:21 GMT
Transfer-Encoding: chunked
*/
// Bun Implementation
function bootstrap1() {
  try {
    // Generate DB
    getOrCreateSqlLite()
    const app = new Elysia()
    app.use(cors())
    app.get('/', AliveController)
    app.get('/health-check', HealthCheckController)

    // @ts-ignore
    app.post('/mcp', async function ({ headers, body }: { headers: Record<string, string>; body: McpRequestTransport }) {
      console.log('---- Incoming Request ----')
      console.log('Headers:', headers)
      console.log('Body:', body)
      console.log('--------------------------')
      const { method, params, id } = body
      const response = {
        jsonrpc: '2.0',
        id,
      } as McpResponseTransport

      switch (method) {
        case 'initialize':
        case 'capabilities':
          console.log('Handling initialize method')
          const result = await CapabilitiesController()

          return {
            ...response,
            result,
          } as McpInitializeMCPServerResponse
        case 'tools/list':
          console.log('Handling tools/list method')
          const tools = await ToolsListingController()
          return {
            ...response,
            result: tools,
          } as McpToolListResponse
        case 'tool/call':
        case 'tools/call':
          console.log('Handling tool/call method')
          const toolres = await ToolCallController({ body: params as unknown as McpToolCallRequest })
          return {
            ...response,
            result: toolres,
          } as McpToolCallResponse
        default:
          console.log(`Unhandled method: ${method}`)
      }

      // handle method: "notifications/initialized"

      return {}
    })
    app.all('*', () => {
      throw new Error('Are You Lost? Have you tried Harry Christner?')
    })
    // app.get('/mcp/capabilities', CapabilitiesController)
    // app.get('/mcp/tools', ToolsListingController)
    // // @ts-ignore
    // app.post('/mcp/tool/call', ToolCallController)
    // // app.get('/mcp/logs', LogsListingController)
    // // app.get('/mcp/prompts', PromptsListingController)
    // // app.get('/mcp/resources', ResourcesListingController)

    app.listen(server_port)

    console.info(`Server is running on http://localhost:${server_port}`)
  } catch (error) {
    console.error('Error during server bootstrap:', error)
    process.exit(1)
  }
}

// Express implemtation
async function bootstrap2() {
  console.log('bootstraping server...')
  const args = process.argv.slice(2)
  const type = args.at(0) || 'http'
  console.log('type:', type)
  if (type === 'http') {
    try {
      // Generate DB
      await getOrCreateSqlLite()
      const app = express()
      app.use(express.json())
      app.use(expressCors()) // Allows all origins
      app.use((req, res, next) => {
        console.log('---- Incoming Request ----')
        reqNum++
        console.log(`Handling request number: ${reqNum}`)
        console.log(`${req.method || 'GET'} ${req.path}`)
        console.log('Headers:', req.headers)
        console.log('Body:', req.body)
        console.log('--------------------------')
        next()
      })

      app.post('/mcp', async (req: express.Request, res: express.Response) => {
        // Create a new transport for each request to prevent request ID collisions
        const transport = new StreamableHTTPServerTransport({
          enableJsonResponse: true,
        })

        res.on('close', () => {
          transport.close()
        })

        // @ts-ignore
        await mcpServer.connect(transport)
        const result = await transport.handleRequest(req, res, req.body)
        console.log('Request handled with result:', result)
      })
      // app.all('*', (req: express.Request) => {
      //   console.log('404 - Not Found:', req.method, req.path)
      //   throw new Error('Are You Lost? Have you tried Harry Christner?')
      // })

      app
        .listen(server_port, () => {
          console.log(`MCP Server running on http://localhost:${server_port}/mcp`)
        })
        .on('error', (error) => {
          console.error('Server error:', error)
          throw error
        })
    } catch (error) {
      console.error('Error during database initialization:', error)
      process.exit(1)
    }
  } else if (type === 'stdio') {
    console.log('stdio transport selected')
    const transport = new StdioServerTransport()
    await mcpServer.connect(transport)
    console.error('MCP Server running on stdio')
  } else {
    throw new Error(`Unknown transport type: ${type}`)
  }
}
bootstrap1()
// bootstrap2()

/*
Request Headers
POST /mcp HTTP/1.1
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Content-Length: 225
Host: localhost:3000
Origin: http://localhost:6274
Referer: http://localhost:6274/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36
accept: application/json, text/event-stream
content-type: application/json
sec-ch-ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "macOS"

Body: {
  jsonrpc: "2.0",
  id: 0,
  method: "initialize",
  params: {
    protocolVersion: "2025-11-25",
    capabilities: {
      sampling: {},
      elicitation: {},
      roots: {
        listChanged: true,
      },
    },
    clientInfo: {
      name: "inspector-client",
      version: "0.18.0",
    },
  },
}
*/

/*
Response Headers
GOOD
HTTP/1.1 200 OK
Access-Control-Allow-Origin: *
Content-Type: application/json
Date: Tue, 06 Jan 2026 23:41:50 GMT
Content-Length: 168
X-Powered-By: Express


BAD
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Vary: *
Access-Control-Allow-Origin: http://localhost:6274
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: host, connection, content-length, user-agent, accept, content-type, origin, sec-fetch-mode, sec-fetch-dest, referer, accept-encoding, accept-language, sec-ch-ua-platform, sec-ch-ua, sec-ch-ua-mobile, sec-fetch-site
Access-Control-Expose-Headers: host, connection, content-length, user-agent, accept, content-type, origin, sec-fetch-mode, sec-fetch-dest, referer, accept-encoding, accept-language, sec-ch-ua-platform, sec-ch-ua, sec-ch-ua-mobile, sec-fetch-site
Content-Type: application/json
Date: Tue, 06 Jan 2026 23:42:05 GMT
Content-Length: 251

Response Body
{
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "service-ninja",
      "version": "1.0.0"
    }
  },
  "jsonrpc": "2.0",
  "id": 0
}
*/
