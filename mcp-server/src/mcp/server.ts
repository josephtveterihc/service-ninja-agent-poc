import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import packageJson from '../../package.json'
import { toolSchemaList } from '../tool-schema'
import type { McpToolSchema } from '../types'
import * as ProjectTools from '../tools/service-ninja/service-ninja-project.tool'
import * as EnvironmentTools from '../tools/service-ninja/service-ninja-environment.tool'
import * as ResourceTools from '../tools/service-ninja/service-ninja-resource.tool'
import * as ResourceContactTools from '../tools/service-ninja/service-ninja-resource-contact.tool'
import * as ContactTools from '../tools/service-ninja/service-ninja-contact.tool'
import * as ResourceMonitorTools from '../tools/resource_monitor.tool'
import { jsonSchemaToZod } from '@n8n/json-schema-to-zod'

// Create server instance
export const mcpServer = new McpServer({
  name: 'service-ninja',
  version: packageJson.version,
})

function getToolFunctionByName(functionName: string) {
  const toolArray = [ProjectTools, EnvironmentTools, ResourceTools, ResourceContactTools, ContactTools, ResourceMonitorTools]
  for (const toolModule of toolArray) {
    if (functionName in toolModule) {
      // @ts-expect-error - We have already checked that the function exists in the module
      return toolModule[functionName]
    }
  }
  return null
}

function initializeServer() {
  console.log('--- Initializing MCP Server ---')
  // Register tool schemas
  toolSchemaList.forEach((toolSchema: McpToolSchema) => {
    const { name, description, inputSchema, functionName } = toolSchema
    if (!functionName) {
      console.warn(`--- Tool ${name} is missing functionName, skipping registration ---`)
      return
    }
    const toolFunction = getToolFunctionByName(functionName)
    if (!toolFunction) {
      console.warn(`--- Tool function ${functionName} for tool ${name} not found, skipping registration ---`)
      return
    }
    const module = jsonSchemaToZod(inputSchema)
    mcpServer.registerTool(
      name,
      {
        title: name,
        description,
        inputSchema: module,
      },
      toolFunction
    )
  })
}

initializeServer()
// mcpServer.registerTool(
//   'get_weather',
//   {
//     title: 'Get Weather',
//     description: 'Get weather information for a given location',
//     inputSchema: {
//       location: z.string().describe('Location to get weather for, e.g., city name, state, or coordinates'),
//     },
//   },
//   async ({ location }) => {
//     if (!location) {
//       return {
//         content: [
//           {
//             type: 'text',
//             text: 'Location is required.',
//           },
//         ],
//       }
//     }

//     // mock weather data
//     const conditions = ['Sunny', 'Rainy', 'Cloudy', 'Snowy']
//     const weather = {
//       location: location,
//       temperature: `${Math.floor(Math.random() * 80) + 10}°F`,
//       condition: conditions[Math.floor(Math.random() * conditions.length)],
//     }
//     return {
//       content: [
//         {
//           type: 'text',
//           text: JSON.stringify(weather),
//         },
//       ],
//     }
//   }
// )
