import { Elysia } from 'elysia'
import * as DotEnv from 'dotenv'
import { HealthCheckController } from './src/controller/health-check.controller'
import { AliveController } from './src/controller/alive.controller'
import { CapabilitiesController } from './src/controller/capabilities.controller'
import { ToolsListingController } from './src/controller/tools-listing.controller'
import { ToolCallController } from './src/controller/tool-call.controller'
import { getOrCreateSqlLite } from './src/sql-lite/sql-lite.init'

DotEnv.config()

const server_port = process.env.SERVER_PORT || 3000

function bootstrap() {
  try {
    // Generate DB
    getOrCreateSqlLite()
    const app = new Elysia()

    app.get('/', AliveController)
    app.get('/health-check', HealthCheckController)

    app.all('*', () => {
      throw new Error('Are You Lost? Have you tried Harry Christner?')
    })

    app.get('/mcp/capabilities', CapabilitiesController)
    app.get('/mcp/tools', ToolsListingController)
    // @ts-ignore
    app.post('/mcp/tool/call', ToolCallController)
    // app.get('/mcp/logs', LogsListingController)
    // app.get('/mcp/prompts', PromptsListingController)
    // app.get('/mcp/resources', ResourcesListingController)

    app.listen(server_port)

    console.info(`Server is running on http://localhost:${server_port}`)
  } catch (error) {
    console.error('Error during server bootstrap:', error)
    process.exit(1)
  }
}
bootstrap()
